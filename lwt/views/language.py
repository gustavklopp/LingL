# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db import transaction
from django.db.models import Q, Value, Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language
from  django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # used for pagination (on text_list for ex.)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder # to json.dumps a datetime object
from django.utils.translation import gettext as _
from django.contrib import messages
from django.urls import reverse
# second party
import os
import json # it's standard in python
import re
# third party
import yaml # pipenv install pyyaml
# local
from lwt.models import *
from lwt.forms import make_languagesform

# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import get_word_database_size
from test.test_sys_settrace import called


# display a table containing all the languages of the User
@login_required
def language_list(request):
    # make the language currentlanguage.
    # via icon set current in language_list: {% url 'language_list' %}?setcurrentlang=lgid  
    if request.GET.get('setcurrentlang'): 
        lgid = request.GET['setcurrentlang'] 
        # and put that inside database and cookie:
        setter_settings_cookie_and_db('setcurrentlang', lgid, request)
        
    #TODO: delete a language, "refresh a language: ???
    if request.GET.get('refresh'): 
        pass
    
    if request.GET.get('delete'): 
        ids_to_delete = request.GET['delete']
        ids_to_delete = json.loads(ids_to_delete)
        dellang_nb = 0
        for lang_id in ids_to_delete:
            # get the list of all ids of the words. They will be used to delete the grouper_of_same_word
            # since they are base on the ids of Words:
            deleted_word_ids = Words.objects.filter(owner=request.user).filter(language_id=lang_id).values_list('id')
            # then delete Words...
            Words.objects.filter(owner=request.user).filter(language_id=lang_id).delete()
            # Grouper of same words
            for id in deleted_word_ids:
                Grouper_of_same_words.objects.get(id=id).delete() # than grouper_of_same_word
            # sentences...
            Sentences.objects.filter(owner=request.user).filter(language_id=lang_id).delete()
            # texts...
            Texts.objects.filter(owner=request.user).filter(language_id=lang_id).delete()
            # and finally languages:
            dellang = Languages.objects.filter(owner=request.user).filter(id=lang_id).delete()
            dellang_nb += dellang[0]

        messages.add_message(request, messages.SUCCESS, str(dellang_nb) + _(' Language(s) successfully deleted / '))

    # For DISPLAY all the languages
    all_languages = Languages.objects.filter(owner=request.user).all().order_by('name') # Don't use the cookie: we need all the info from Lanuguages!

    ##############################display some stats about the Languages: ############################################
    all_languages_dict = []
    for lang in all_languages:
        word_count = Words.objects.filter(language=lang).\
                                exclude(Q(isnotword=True)&Q(isCompoundword=False)).count()
        all_languages_dict.append({'lang':lang,'word_count':word_count})
    # get currentlang_id from cookie, else from database
    currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)

    # get the current database size:
    database_size = get_word_database_size(request)

    return render(request, 'lwt/language_list.html',{'all_languages_dict':all_languages_dict,
                                                     'currentlang_id':currentlang_id,
                                                 'database_size':database_size})

# languages detail: edit/create a language
@login_required
def language_detail(request):
    #### PROCESSING THE SENT FORM (= clicked on 'save' button)#################
    if request.method == 'POST': 
                
        if 'new' in request.GET.keys(): # saving a New language:
            f = make_languagesform(request.user.id)(request.POST or None)
            if f.is_valid():
                savedlanguage = f.save()
                # manually saving the fields because Modelform is not saving (I don't know why...)
                savedlanguage.__dict__.update(f.cleaned_data)
                savedlanguage.owner = request.user
                savedlanguage.save()
                messages.add_message(request, messages.SUCCESS, _('Language successfully created'))
        elif 'edit' in request.GET.keys(): # editing an existing language:
            existinglanguage = Languages.objects.get(id=request.GET['edit'])
            f = make_languagesform(request.user.id)(request.POST, instance=existinglanguage)
            if f.is_valid():
                savedlanguage = f.save(commit=False)
                existinglanguage = Languages.objects.get(id=request.GET['edit'])
                savedlanguage.id = existinglanguage.id #request.GET['edit'] is the id of the existing lang
                savedlanguage.created_date = existinglanguage.created_date 
                savedlanguage.save()
                messages.add_message(request, messages.SUCCESS, _('Language successfully edited'))
        # and put that inside database and cookie:
        setter_settings_cookie_and_db('currentlang_id', savedlanguage.id, request)
        ############## EDIINTG THE JSON EXTRA FIELD in WORDS #########################################
        # only if there are words already defined of course and if this extra fields has been defined:
        thislang_words = Words.objects.filter(language=savedlanguage).\
                            exclude(Q(isnotword=True)&Q(isCompoundword=False)).all()
        #TODO Extra fields
#             
#             if thislang_words and thislang_words.first():
#                 old_extra_field_json = thislang_words.first().extra_field
#                 extra_field_key_list = []
#                 extra_field_list = json.loads(old_extra_field_json) if old_extra_field_json else []
#                 for extra_field_key in savedlanguage.extra_field_key:
#                     extra_field_key_list.append(extra_field_key.title)
#                     ############################# creating a new extra field: ###############################################
#                     if extra_field_key.title not in old_extra_field_json: # we add an additional field
#                         # we don't load the json, only using the string to skip some steps.
#                         extra_field_list.append({extra_field_key.title:''})
#                         def insert_key(old_key):
#                             ''' update the json dictionary with the new key'''
#                             if old_key:
#                                 new_key = old_key[:-1] + ',{"'+extra_field_key.title+'":""}'+old_key[-1]
#                             else: # there's no key before
#                                 new_key = '[{"'+extra_field_key.title+'":""}]'
#         #                     new_key = '[{"'+extra_field_new+'":""}]'
#                             return new_key
#                         with transaction.atomic():
#                             for thislang_word in thislang_words: # update all the words
#                                 new_extra_field_json = thislang_word.extra_field
#                                 thislang_word.extra_field = insert_key(new_extra_field_json)
#                                 thislang_word.save()
# 
#                 ################################ deleting an existing extra field: ##########################################
#                 key_to_delete_list = []
#                 for el_dict in extra_field_list: # it's the fist word's extrafield that we use as representation of all the other
#                     key_to_test = list(el_dict.keys())[0]
#                     if  key_to_test not in extra_field_key_list: # delete it
#                         key_to_delete_list.append(key_to_test)
#                         # remove from the list
#                 if key_to_delete_list:
#                     with transaction.atomic():
#                         for thislang_word in thislang_words: # update all the words
#                             old_extra_field_json = thislang_words.extra_field
#                             extra_field_list = yaml.loads(old_extra_field_json) if old_extra_field_json else []
#                             # we keep only the keys existing in Language.extra_field
#                             new_extra_field_list = [el for el in extra_field_list if list(el.keys())[0] in key_to_delete_list]
#                             thislang_word.extra_field = yaml.dumps(new_extra_field_list)
#                             thislang_word.save()

        if f.is_valid():
            return redirect(reverse('language_list'))
        else:
            return render(request, 'lwt/language_detail.html', {'form':f})

    #### DISPLAYING THE FORM #################
    elif request.method == 'GET':
        extra_field_list = []
#         lang_id = ''
        # a new language is requested:
        if 'new' in request.GET.keys():
            # always set the owner as default request.user
            f = make_languagesform(request.user.id)(initial = { 'owner': request.user.id })
            # STRING CONSTANTS:
            op = 'new'
        if 'edit' in request.GET.keys():
            lang_id = int(request.GET['edit'])
            lang_query = Languages.objects.filter(id=lang_id)
            lang_Obj = lang_query[0] 
            lang = lang_query.values()[0] # we need a dict for the operation below
            if lang['code_639_1']: # if it's defined of course
                # we get the fixture to add uris to the dropdown menus if the user wants to change it
                chosen_lang = substitute_in_dictURI(request.user, lang['code_639_1'])
                chosen_lang_datalist = [[i,i] for i in chosen_lang['dicturi'].split(',')]
            else:
                chosen_lang_datalist = []
            # we pre-initialized LanguagesForm with datalist for the dropdowntoggle widget
            f = make_languagesform(request.user.id, dicturi_list=chosen_lang_datalist)(
                                    instance= lang_Obj)
            # STRING CONSTANTS:
            op = 'edit'
    # get all the languages (used for javascript script to check no doublon)
    all_languages = Languages.objects.all()

    # get the current database size:
    database_size = get_word_database_size(request)

    return render(request, template_name='lwt/language_detail.html', context={
        'all_languages':all_languages, 'form': f,
        'origin_lang_code': request.user.origin_lang_code,
#         'extra_field_list':extra_field_list, 
#         'lang_id': lang_id, # used to post extra field with the correct language
        # STRING CONSTANTS:
        'op':op, 'database_size':database_size}
#         , renderer=None,
     
     )

''' requested by ajax_fill_language_detail: a code_lang is sent, get all the data for the language '''
def fill_language_detail(request):
    code_lang = request.GET['code_lang'] #for example: code_lang = 'si'
    chosen_lang = substitute_in_dictURI(request.user, code_lang)
    js = json.dumps(chosen_lang, cls=DjangoJSONEncoder)
    return HttpResponse(js)



    
    