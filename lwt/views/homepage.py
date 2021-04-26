# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db.models import Q, Value, Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # used for pagination (on text_list for ex.)
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.serializers import serialize
from django.utils import timezone

from django.http import HttpResponse
# second party
import gzip
import io
# third party)
# local
from lwt.models import *
from lwt.forms import *

# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import get_word_database_size


''' Home Page '''
@login_required
def homepage(request):
    # User wants to change the language:
    if request.GET.get('setcurrentlang'):
        lgid = int(request.GET['setcurrentlang'])
        # and put that inside database and cookie:
        setter_settings_cookie_and_db('currentlang_id', lgid, request)
        currentlang_id = lgid
        if lgid == -1: # -1 is the code for: Filter Off
            currentlang_name = -1 
            currentlang_id = -1
        else:
            # update currentlang_id and currentlang_name:
            currentlang_id = lgid
            currentlang_name = Languages.objects.values_list('name',flat=True).get(id=lgid)
    else:
        # get the currentlang.
        currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)
        if currentlang_id == '': # first time launching: no Language.
            currentlang_name = ''
        else: # Languages exist
            if int(currentlang_id) == -1: # -1 is the code for no filter 
                currentlang_name = -1
            else: # "" is the code for : not yet defined
                currentlang_name = Languages.objects.filter(owner=request.user).values_list('name',flat=True).get(id=currentlang_id) if currentlang_id else ""

    # Last open texts:
    lastopentexts = Texts.objects.filter(owner=request.user, lastopentime__isnull=False).order_by('lastopentime').all()[:5]

    # get the list of languages to display them in the drop-down menu:
    language_selectoption = Languages.objects.filter(owner=request.user).values('name','id').order_by('name')
    
    # get the current database size:
    database_size = get_word_database_size(request)

    return render(request, 'lwt/homepage.html', {'currentlang_name':currentlang_name,'currentlang_id':currentlang_id,
                                                 'lastopentexts':lastopentexts, 
                                                 'language_selectoption':language_selectoption,
                                                 'database_size':database_size})

