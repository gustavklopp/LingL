# django:
from django.core.serializers import serialize
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db.models import Q, Value, Count
from django.db.models.functions import Lower 
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from django.apps import apps
# second party
import os
import gzip #it's standard in python
import io #it's standard in python
import tempfile #it's standard in python
# third party
from yaml import load, Loader, FullLoader
# local
from lwt.models import *
from lwt.forms import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from lwt.views._nolang_redirect_decorator import *
from lwt.views._import_oldlwt import *


''' delete all the data (except MyUser * Settings_... (but all Settings_current are deleted)) '''
def wipeout_database(request, keep_myuser=False):
    for mymodel in apps.get_app_config('lwt').get_models():
        if mymodel == Uploaded_text: 
            # don't delete the Uploaded_text models:
            continue
        elif mymodel == MyUser: 
            if not keep_myuser:
                mymodel.objects.get(id=request.user.id).delete()
            else:
                continue
        else:
            mymodel.objects.filter(owner=request.user).all().delete()
    #update the cookie for the database_size
    set_word_database_size(request)
    # and delete cookies:
    if 'currentlang_id' in request.session.keys(): # if the session has been defined
        del request.session['currentlang_id'] 
        request.session.modified = True
    if 'currentlang_name' in request.session.keys(): # if the session has been defined
        del request.session['currentlang_name']
        request.session.modified = True

''' gunzip (=decompress a gzipped file) the file uploaded'''
def gunzipper(data_file):
    fp = tempfile.NamedTemporaryFile(suffix='.yaml')
    with gzip.open(data_file.path, 'r') as f:
        fp.write(f.read())
    fp.seek(0) # obligatory to rewind the file after having been read/written
    return fp

""" Backup/restore """
def backuprestore(request):
    if request.method == 'POST':
        # backing up:
        if 'backingup' in request.POST.values():
            all_qs = []

            for mymodel in apps.get_app_config('lwt').get_models():
                if mymodel == MyUser:
                    all_qs += mymodel.objects.filter(username=request.user.username)
#                 elif mymodel == Restore or mymodel == Uploaded_text or \
#                     mymodel == Grouper_of_same_words: 
                # don't back up Restore and Uploaded_text models:
                elif mymodel == Restore or mymodel == Uploaded_text:
                    continue
                else:
                    all_qs += mymodel.objects.filter(owner=request.user).all()
            fixture = serialize('yaml', all_qs, use_natural_foreign_keys=True, use_natural_primary_keys=True)
            # Set the FK Grouper_of_same_word to null (we'll relink them when recovering the file)
            # (it's because we can't use natural FK since GOSW use a id number relationship)
            fixture = re.sub(r'(grouper_of_same_words: )\d+', r'\1null', fixture)
            now = timezone.now().strftime('%Y-%m-%d_%Hh%M') 
            filename = 'lingl_backup_{}.yaml.gz'.format(now)
            out = io.BytesIO()
            with gzip.GzipFile(fileobj=out, mode='w') as f:
                f.write(fixture.encode())
            response = HttpResponse(out.getvalue(), content_type='application/gzip')
            response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
            return response

        # Empty the database:
        if 'empty' in request.POST.values():
            wipeout_database(request)
            return redirect(reverse('homepage'))

        if 'restore' in request.POST.values():
            form = RestoreForm(request.POST, request.FILES)
            if form.is_valid():
                files = form.save()
                # process the uploaded file if it exists:
                wipeout_database(request, keep_myuser=True)
                fp = gunzipper(files.restore_file)
                # Don´t install the User defined in the Restore file and change all the
                # owner of the Restore file to the current User
                editedOwner_fp = os.path.join(settings.MEDIA_ROOT, 'editedOwner_{}.yaml'.format(request.user))
                start_writing = False
                restore_username = request.user.username # the default value
                with open(editedOwner_fp, 'w') as edited_f:
                    for line in fp.file.readlines():
                        line = line.decode('utf-8') # the line in this file are binary: b'my text...'
                        # get the username from the restore file ...
                        if not start_writing:
                            match = re.search(r'(?<=username: )\w+', line)
                            if match:
                                restore_username = match.group()
                            # all the MyUser section of the restore file is ignored
                            if line.find('lwt.languages') != -1:
                                start_writing = True
                                edited_f.write(line)
                        else:
                            # and substitute it with the current User
                            pattern = r'(^[ -]+- ){}'.format(restore_username)
                            replacement = r'\1{}'.format(request.user.username)
                            line = re.sub(pattern, replacement, line)
                            edited_f.write(line)
#                     call_command('loaddata', fp.name, app_label='lwt') # load the fixtures
                    call_command('loaddata', editedOwner_fp, app_label='lwt') # load the fixtures
                fp.close()
                delete_uploadedfiles(files.restore_file.path, request.user) # clean it
                os.remove(editedOwner_fp)

                # then create grouper_of_same_words: it's a copy of Words' ids.
                # create the GOSW...
#                 words = Words.objects.filter(Q(owner=request.user)&Q(isnotword=False))
#                 create_GOSW_for_words(words)

            # set arbitrary the currentlang
            lang = Languages.objects.filter(owner=request.user).first()
            setter_settings_cookie('currentlang_id', lang.id, request)
            setter_settings_cookie('currentlang_name', lang.name, request)

        #TODO! NOT FINISHED
        if 'import_oldlwt' in request.POST.values():
            fp = gunzipper(files.import_oldlwt)
            import_oldlwt(request.user, fp)
            fp.close()
            delete_uploadedfiles(fp.name, request.user)
        
        if 'install_demo' in request.POST.values():
            # First, install the languages (must change the owner):
            user_username = str(request.user.username)

            # put a temporary name for the already defined language by the User
            # (else it will create a non unique constraint error when importing the language fixture
            dest_chosen_lang = Languages.objects.get(owner=request.user)
            temp_name = dest_chosen_lang.name
            dest_chosen_lang.name = "{}_{}".format(temp_name, user_username)
            dest_chosen_lang.save()

            lang_fixt_path = 'lwt/fixtures/initial_fixture_LANGUAGES.yaml'
            USER_lang_fixt_path = 'lwt/fixtures/initial_fixture_LANGUAGES_{}.yaml'.format(user_username)

            with open(lang_fixt_path) as lang_fixt_file:
                langs = lang_fixt_file.read()
                langs = langs.replace("- lingl", "- {}".format(user_username))
                with open(USER_lang_fixt_path, "w") as USER_lang_fixt_file:
                    USER_lang_fixt_file.write(langs)
            call_command('loaddata', USER_lang_fixt_path , app_label='lwt') # load the fixtures
            os.remove(USER_lang_fixt_path)
             
            # then, install all the Demo, except the Grouper_of_same_words (we will create them manually):
            demo_fixt_path = 'lwt/fixtures/oldlwt_fixture_demo.yaml'
            USER_demo_fixt_path = 'lwt/fixtures/oldlwt_fixture_demo_{}.yaml'.format(user_username)

            with open(demo_fixt_path) as demo_fixt_file:
                demo = demo_fixt_file.read()
                demo = demo.replace("- lingl", "- {}".format(user_username))
                with open(USER_demo_fixt_path, "w") as USER_demo_fixt_file:
                    USER_demo_fixt_file.write(demo)
            call_command('loaddata', USER_demo_fixt_path , app_label='lwt') # load the fixtures
            os.remove(USER_demo_fixt_path)
            
#                 # then grouper_of_same_words: it's a copy of Words' ids.
#                 # create the GOSW...
#                 words = Words.objects.filter(Q(owner=request.user)&Q(isnotword=False))
#                 create_GOSW_for_words(words)
            
            # the language chosen initially for the User is in double: remove it
            # (it was first created when the User is signing up)
            Languages.objects.filter(Q(owner=request.user)&Q(name=temp_name)).order_by('-created_date').first().delete()
            # and put again the name of the language, changed at the start to avoid unique constraint error
            dest_chosen_lang.name = temp_name
            dest_chosen_lang.save()

#             if set(['import_oldlwt','install_demo','restore']) & set(request.POST.values()):
#                 # set the currentlang if not aloready defined
#                 owner = request.user
#                 lang = Languages.objects.get(owner=owner, django_code=owner.origin_lang_code)
#                 setter_settings_cookie_and_db('currentlang_id', lang.id, request, owner)

        return redirect(reverse('homepage'))

    else:
        form = RestoreForm()
            
    # get the current database size:
    database_size = get_word_database_size(request)

    return render(request, 'lwt/backuprestore.html', {'form': form,
                                                 'database_size':database_size})

