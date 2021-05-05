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
# local
from lwt.models import *
from lwt.forms import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from lwt.views._nolang_redirect_decorator import *
from lwt.views._import_oldlwt import *


''' delete all the data (except MyUser * Settings_... (but all Settings_current are deleted)) '''
def wipeout_database(request):
    for mymodel in apps.get_app_config('lwt').get_models():
        if mymodel == MyUser: # don't delete the MyUser
            continue
        mymodel.objects.filter(owner=request.user).all().delete()
    #update the cookie for the database_size
    set_word_database_size(request)
    # and delete cookies:
    if 'currentlang_id' in request.session.keys(): # if the session has been defined
        del request.session['currentlang_id'] 
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
                all_qs += mymodel.objects.filter(owner=request.user).all()
            fixture = serialize('yaml', all_qs)
            now = timezone.now().strftime('%Y-%m-%d') 
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
        form = RestoreForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.save()
            # process the uploaded file if it exists:
            if 'restore' in request.POST.values():
                wipeout_database(request)
                fp = gunzipper(files.restore_file)
                call_command('loaddata', fp.name, app_label='lwt') # load the fixtures
                fp.close()
                delete_uploadedfiles(Restore) # clean it

            if 'import_oldlwt' in request.POST.values():
                fp = gunzipper(files.import_oldlwt)
                import_oldlwt(request.user, fp)
                fp.close()
                delete_uploadedfiles(Restore)
            
            if 'install_demo' in request.POST.values():
                # make the user the owner of the elements in the fixture
                fixt = 'lwt/fixtures/lingl_demo_user_1.yaml'
                user_id = str(request.user.id)
                fixt_copy = fixt.replace("1", user_id)
                with open(fixt, "r") as fixt_file:
                    texts = fixt_file.read()
                    texts = texts.replace("owner: 1", "owner: "+user_id)
                with open(fixt_copy, "w") as fixtCopy_file:
                    fixtCopy_file.write(texts)
                call_command('loaddata', fixt_copy , app_label='lwt') # load the fixtures
                os.remove(fixt_copy)
                # the language chosen initially for the User is in double: remove it
                # (it was first loaded by 'initial_fixture.yaml')
                Languages.objects.filter(owner=request.user).order_by('-created_date').first().delete()

            if set(['import_oldlwt','install_demo','restore']) & set(request.POST.values()):
                # set the currentlang if not aloready defined
                owner = request.user
                lang = Languages.objects.get(owner=owner, django_code=owner.origin_lang_code)
                setter_settings_cookie_and_db('currentlang_id', lang.id, request, owner)
            
            if set(['install_demo','restore']) & set(request.POST.values()):
                # set the current user:
                logout(request)
                login(request, owner, backend='allauth.account.auth_backends.AuthenticationBackend' )

            return redirect(reverse('homepage'))
    else:
        form = RestoreForm()
            
    # get the current database size:
    database_size = get_word_database_size(request)

    return render(request, 'lwt/backuprestore.html', {'form': form,
                                                 'database_size':database_size})

