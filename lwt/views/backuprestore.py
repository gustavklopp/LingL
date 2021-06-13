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
from django.utils.translation import ugettext as _, ngettext
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from django.apps import apps
from django.templatetags.static import static # to use the 'static' tag as in the templates
from django.contrib import messages
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
from tkinter.constants import CURRENT
#from MySQLdb._mysql import result


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
    with gzip.open(data_file.path, 'r', encoding="utf8") as f:
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
#             # Set the FK Grouper_of_same_word to null (we'll relink them when recovering the file)
#             # (it's because we can't use natural FK since GOSW use a id number relationship)
#             fixture = re.sub(r'(grouper_of_same_words: )\d+', r'\1null', fixture)
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
            messages.add_message(request, messages.SUCCESS, _('Account successfully deleted.'))
            return redirect(reverse('homepage'))

        if 'restore_data' in request.POST.keys() and request.POST['restore_data'] != '':
            need_text = True if request.POST['restore_data'] == 'word+text' else False
            form = RestoreForm(request.POST, request.FILES)
            if form.is_valid():
                files = form.save()
                # process the uploaded file if it exists:
#                 wipeout_database(request, keep_myuser=True)
                fp = gunzipper(files.restore_file)
                # Don´t install the User defined in the Restore file and change all the
                # owner of the Restore file to the current User
                editedOwner_fp = os.path.join(settings.MEDIA_ROOT, 'editedOwner_{}.yaml'.format(request.user))
                current_section = ''
                writing = True
                restore_username = request.user.username # the default value
                with open(editedOwner_fp, 'w', encoding="utf8") as edited_f:
                    for line in fp.file.readlines():
                        line = line.decode('utf-8') # the line in this file are binary: b'my text...'

                        current_section_match = re.search(r'(?<=lwt\.)\w+', line)
                        if current_section_match:
                            current_section = current_section_match.group()

                        # get the username from the restore file ...
                        if current_section == 'myuser':
                            match = re.search(r'(?<=username: )\w+', line)
                            if match:
                                restore_username = match.group()
                        else:
                            # and substitute the username found in the restore file by the current User
                            pattern = r'(^[ -]+- ){}'.format(restore_username)
                            replacement = r'\1{}'.format(request.user.username)
                            line = re.sub(pattern, replacement, line)

                            if not need_text:
                                # don't write Texts and Sentences if not chosen:
                                if current_section == 'texts' or current_section == 'sentences':
                                    continue
                                if current_section == 'words':
                                    # set to null the fields in Words for 'text' and 'sentence'
                                    match = re.search(r'^    text:', line)
                                    if match:
                                        writing = False
                                        writing_counter = 0
                                    if not writing:
                                        writing_counter += 1
                                        if writing_counter == 8:
                                            writing = True
                                            edited_f.write('    text: null\n')
                                            edited_f.write('    sentence: null\n')
                                    else:
                                        # set to null the fields in Words for 'order' and 'textOrder'
                                        line = re.sub(r'(^    order: )\d+', r'\1null' , line)
                                        line = re.sub(r'(^    textOrder: )\d+', r'\1null' , line)
                                        edited_f.write(line)

                                else:
                                    edited_f.write(line)
                                    
                                    
                            else:
                                edited_f.write(line)
                call_command('loaddata', editedOwner_fp, app_label='lwt') # load the fixtures
                fp.close()
                # clean it
                delete_uploadedfiles(files.restore_file.path, request.user) 
                os.remove(editedOwner_fp)

                messages.add_message(request, messages.SUCCESS, _('Import of backup file successful.'))

            # set arbitrary the currentlang
            lang = Languages.objects.filter(owner=request.user).first()
            setter_settings_cookie('currentlang_id', lang.id, request)
            setter_settings_cookie('currentlang_name', lang.name, request)

        if 'import_oldlwt' in request.POST.values() and request.POST['import_oldlwt'] != '':
            form = RestoreForm(request.POST, request.FILES)
            if form.is_valid():
                files = form.save()
                # process the uploaded file if it exists:
#                 wipeout_database(request, keep_myuser=True)
                fp = gunzipper(files.import_oldlwt)
                result_nb = import_oldlwt(request.user, fp)
                fp.close()
                # clean it
                delete_uploadedfiles(files.import_oldlwt.path, request.user) # clean it

                m = _('Successful import of old lwt : ')
                m += ngettext('%(count)d language, ', '%(count)d languages, ',
                                result_nb['createdLanguage_nb']) % {'count': result_nb['createdLanguage_nb']}                    
                m += ngettext('%(count)d text, ', '%(count)d texts, ',
                                result_nb['createdText_nb']) % {'count': result_nb['createdText_nb']}                    
                m += ngettext('%(count)d word was imported.', '%(count)d words were imported.',
                                result_nb['createdWord_nb']) % {'count': result_nb['createdWord_nb']}                    
                messages.add_message(request, messages.SUCCESS, m)
        
        if 'install_demo' in request.POST.values():
            # First, install the languages (must change the owner):
            user_username = str(request.user.username)

            #########################
            # Rename with a temporary name for the already defined language by the User
            # (for ex: English ==> English_franck)
            # (else it will create a non unique constraint error when importing the language fixture
            dest_chosen_lang = Languages.objects.get(owner=request.user)
            temp_name = dest_chosen_lang.name
            dest_chosen_lang.name = "{}_{}".format(temp_name, user_username)
            dest_chosen_lang.save()

            # the User is the owner of these languages we'll import
            lang_fixt_path = os.path.join(settings.BASE_DIR, 'lwt','fixtures','initial_fixture_LANGUAGES.yaml')
            USER_lang_fixt_path = lang_fixt_path.replace('.yaml','_{}.yaml'.format(user_username))

            with open(lang_fixt_path, encoding="utf8") as lang_fixt_file:
                langs = lang_fixt_file.read()
                # replace the owner username
                langs = langs.replace("- lingl", "- {}".format(user_username))
                with open(USER_lang_fixt_path, "w", encoding="utf8") as USER_lang_fixt_file:
                    USER_lang_fixt_file.write(langs)
            call_command('loaddata', USER_lang_fixt_path , app_label='lwt') # load the fixtures
            os.remove(USER_lang_fixt_path)
            
            #########################
            # the user languages needs the correct dict URIs with the User's origin lang:
            for lang in Languages.objects.filter(owner=request.user):
                lang = substitute_in_dictURI(request.user, lang, called_by_Obj=True)
                # and put it in dict1uri and dict2uri also
                dicturi = lang.dicturi.split(',')
                lang.dict1uri = dicturi[0].strip()
                lang.dict2uri = dicturi[1].strip()
                lang.save()
             
            ##########################
            # then, install all the Demo, except the Grouper_of_same_words (we will create them manually):
            demo_fixt_path = os.path.join(settings.BASE_DIR, 'lwt','fixtures', 'oldlwt_fixture_demo.yaml')
            USER_demo_fixt_path = demo_fixt_path.replace('.yaml','_{}.yaml'.format(user_username))

            with open(demo_fixt_path, encoding="utf8") as demo_fixt_file:
                demo = demo_fixt_file.read()
                demo = demo.replace("- lingl", "- {}".format(user_username))
                with open(USER_demo_fixt_path, "w", encoding="utf8") as USER_demo_fixt_file:
                    USER_demo_fixt_file.write(demo)
            call_command('loaddata', USER_demo_fixt_path , app_label='lwt') # load the fixtures
            os.remove(USER_demo_fixt_path)
            
            # the language chosen initially for the User is in double: remove it
            # (it was first created when the User is signing up)
            Languages.objects.filter(Q(owner=request.user)&Q(name=temp_name)).order_by('-created_date').first().delete()
            # and put again the name of the language, changed at the start to avoid unique constraint error
            dest_chosen_lang.name = temp_name
            dest_chosen_lang.save()
            
            # don't know why but I need to re-login...
            logout(request)
            myuser = MyUser.objects.get(username=user_username)
            login(request, myuser, backend='allauth.account.auth_backends.AuthenticationBackend' )

            messages.add_message(request, messages.SUCCESS, _('Demo successfully installed.'))
            
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

