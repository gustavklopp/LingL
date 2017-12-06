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
# second party
import json
import re
# third party
# local
from lwt.models import *
from lwt.forms import *

# helper functions:
from lwt.views._setting_cookie_db import *


# languages list
@login_required
def language_list(request):
    # make the language currentlanguage.
    # via new lang from language_detail:  {% url 'language_list' %}?setcurrentlang=newlang  
    # via icon set current in language_list: {% url 'language_list' %}?setcurrentlang=lgid  
    if request.GET.get('setcurrentlang'): 
        if request.GET['setcurrentlang'] == 'newlang': # Language_detail asked a new language
            lgid = savednewlang.id
        else:   # asked via the icon in language_list
            lgid = request.GET['setcurrentlang'] 
        # and put that inside database and cookie:
        setter_settings_cookie_and_db('setcurrentlang', lgid,request)
        
    #TODO: delete a language, "refresh a language: ???
    if request.GET.get('refresh'): 
        pass
    
    if request.GET.get('delete'): 
        ids_to_delete = request.GET['del']
        ids_to_delete = json.loads(ids_to_delete)
        dellang_nb = 0
        for lang_id in ids_to_delete:
            # first delete the se with the foreignkeys
            dellang = Languages.objects.filter(owner=request.user).filter(text__id=text_id).delete()
            dellang_nb += dellang[0]
        message =  str(dellang_nb) + _(' Languages deleted / ')

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

    return render(request, 'lwt/language_list.html',{'all_languages_dict':all_languages_dict,
                                                     'currentlang_id':currentlang_id})

# languages detail: edit/create a language
@login_required
def language_detail(request):
    if request.method == 'POST':
                
        f = make_languagesform()(request.POST or None)
        if f.is_valid():
            savedlanguage = f.save()
            # and put that inside database and cookie:
            setter_settings_cookie_and_db('setcurrentlang', savedlanguage.id,request)
            ############## EDIINTG THE JSON EXTRA FIELD in WORDS #########################################
            # only if there are words already defined of course:
            thislang_words = Words.objects.filter(language=savedlanguage).\
                                exclude(Q(isnotword=True)&Q(isCompoundword=False)).all()
            if thislang_words:
                extra_field_key_list = []
                old_extra_field_json = thislang_words.first().extra_field
                extra_field_list = json.loads(old_extra_field_json) if old_extra_field_json else []
                for extra_field_key in savedlanguage.extra_field_key:
                    extra_field_key_list.append(extra_field_key.title)
                    ############################# creating a new extra field: ###############################################
                    if extra_field_key.title not in old_extra_field_json: # we add an additional field
                        # we don't load the json, only using the string to skip some steps.
                        extra_field_list.append({extra_field_key.title:''})
                        def insert_key(old_key):
                            ''' update the json dictionary with the new key'''
                            if old_key:
                                new_key = old_key[:-1] + ',{"'+extra_field_key.title+'":""}'+old_key[-1]
                            else: # there's no key before
                                new_key = '[{"'+extra_field_key.title+'":""}]'
        #                     new_key = '[{"'+extra_field_new+'":""}]'
                            return new_key
                        with transaction.atomic():
                            for thislang_word in thislang_words: # update all the words
                                new_extra_field_json = thislang_word.extra_field
                                thislang_word.extra_field = insert_key(new_extra_field_json)
                                thislang_word.save()

                ################################ deleteing an existing extra field: ##########################################
                key_to_delete_list = []
                for el_dict in extra_field_list: # it's the fist word's extrafield that we use as representation of all the other
                    key_to_test = list(el_dict.keys())[0]
                    if  key_to_test not in extra_field_key_list: # delete it
                        key_to_delete_list.append(key_to_test)
                        # remove from the list
                if key_to_delete_list:
                    with transaction.atomic():
                        for thislang_word in thislang_words: # update all the words
                            old_extra_field_json = thislang_words.extra_field
                            extra_field_list = json.loads(old_extra_field_json) if old_extra_field_json else []
                            # we keep only the keys existing in Language.extra_field
                            new_extra_field_list = [el for el in extra_field_list if list(el.keys())[0] in key_to_delete_list]
                            thislang_word.extra_field = json.dumps(new_extra_field_list)
                            thislang_word.save()
            return redirect(reverse('language_list'))
        else:
            return render(request, 'lwt/language_detail.html', {'form':f})

    elif request.method == 'GET':
        extra_field_list = []
#         lang_id = ''
        # a new language is requested:
        if 'new' in request.GET.keys():
            # always set the owner as default request.user
            f = make_languagesform()(initial = { 'owner': request.user })
            # STRING CONSTANTS:
            op = 'new'
        if 'edit' in request.GET.keys():
#             lang_id = int(request.GET['edit'])
# 

            lang = Languages.objects.filter(id=lang_id).values()[0] # we need a dict for the operation below
            if lang['code_639_1']: # if it's defined of course
                # we get the fixture to add uris to the dropdown menus if the user wants to change it
                chosen_lang = get_language_fixture(request, lang['code_639_1'])
                chosen_lang_datalist = [[i,i] for i in chosen_lang['dicturi']]
            else:
                chosen_lang_datalist = []
            # we pre-initialized LanguagesForm with datalist for the dropdowntoggle widget
            f = make_languagesform(chosen_lang_datalist)(initial = lang)
            # STRING CONSTANTS:
            op = 'edit'
    # get all the languages (used for javascript script to check no doublon)
    all_languages = Languages.objects.all()

    return render(request, 'lwt/language_detail.html', {
        'all_languages':all_languages, 'form': f,
#         'extra_field_list':extra_field_list, 
#         'lang_id': lang_id, # used to post extra field with the correct language
        # STRING CONSTANTS:
        'op':op,
        })

def fill_language_detail(request):
    ''' requested by ajax_fill_language_detail: a code_lang is sent, get all the data for the language '''
    code_lang = request.GET['code_lang']
    chosen_lang = get_language_fixture(request, code_lang)
    js = json.dumps(chosen_lang)
    return HttpResponse(js)

def get_language_fixture(request, code_lang):
    ''' load and get the real name for the Fixtures of languages (in lwt/fixtures folder) '''
    with open('lwt/fixtures/languages_fixtures.json') as lang_json:
        lang_json = lang_json.read()
    languages_fixtures = json.loads(lang_json)
    lang_list = languages_fixtures['_languages']
    # get the destination language for the translation:
    origin_lang_code = request.user.origin_lang_code
    # then get the language data:
    for idx, lang in enumerate(lang_list):
        if lang['code_639_1'] == code_lang:
            chosen_lang = lang_list[idx]
        # and for the origin lang too:
        if lang['code_639_1'] == origin_lang_code:
            origin_lang = lang_list[idx]
    # then change the placeholder string for the translation:
    dicturi_repl_list = []
    for dicturi in chosen_lang['dicturi']:
        dicturi_repl = re.sub(r'•••', origin_lang['code_639_2t'], dicturi)
        dicturi_repl = re.sub(r'••', origin_lang['code_639_1'], dicturi_repl)
        dicturi_repl_list.append(dicturi_repl)
    chosen_lang['dicturi'] = dicturi_repl_list
    return chosen_lang
    
    