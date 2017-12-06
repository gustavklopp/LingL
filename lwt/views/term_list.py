# -*- coding: utf-8 -*-
# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template, render_to_string
from django.db.models import F, Q, Value, Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ExpressionWrapper, F
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # used for pagination (on text_list for ex.)
from django.http import JsonResponse, HttpResponse #used for ajax
from django.utils import timezone, timesince
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# second party
import json
# local
from lwt.models import *
from lwt.forms import *
from lwt.constants import STATUS_CHOICES
# helper functions:
from lwt.views._nolang_redirect_decorator import *
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from ast import parse
from django.http.response import JsonResponse
from django.utils.lorem_ipsum import sentence


def termlist_filter(request):
    ''''the checkboxes to filter the terms '''
    limit = -1

    if 'limit' in request.POST.keys(): # number of rows to display per page
        limit = request.POST['limit']
        limit = int(limit)
    all_words = Words.objects.exclude(Q(isnotword=True)&Q(isCompoundword=False)).\
                            filter(owner=request.user).all()
    all_words = list_filtering(all_words, request) # apply the filtering (it sets also the cookie)
    total = all_words.count()
    all_words = all_words[:limit]
    all_words = serialize_bootstraptable(all_words,total)
    return JsonResponse(all_words, safe=False)
    
def load_wordtable(request):
    ''' called by ajax (built-in function) inside bootstrap-table #word_table to fill the table'''
    order, sort, sort_modif, offset, offset_modif, limit, limit_modif, all_words = requesting_get_by_table(request, Words)

    if 'search' in request.GET.keys():
        search = request.GET['search']
        if search != '': # when deleting the previous search, ajax will send the search word ''. consider it like No filter
            all_words = all_words.filter(wordtext=search)
    all_words = list_filtering(all_words, request) 
    
    # save the total list of item (used for export2anki to get the list of possible selected words):
    possible_selected_rows = list(all_words.values_list('id', flat=True))
    Settings_selected_rows.objects.update_or_create(
        owner=request.user, 
        defaults = {'possible_selected_rows': json.dumps(possible_selected_rows)},
                                                         )

    total = all_words.count() 
    
#         lang_id = getter_settings_cookie('term_list_lang_id', request) # return 'None' if not defined
# 
#         if request.method == 'GET' and 'lang_id' in request.GET.keys():
#             lang_id = int(request.GET['lang_id'])
#             request.session['term_list_lang_id'] = lang_id
# 
#         if lang_id: # by defautl. if the lang has been set in the session, filter on this lang
#             all_words = all_words.filter(language__id=lang_id)
    all_words_filtered = all_words[offset_modif:offset_modif + limit_modif]
    data = []

    def linked(word, original_word):
        ''' create a link inside the bootstrap table: clicking on the word jump to the right place 
       we use 'original_word' only to get the annotation if the sorting is on 'extra_field': indeed,
       we have previously annotated 'original_word' with the key form 'extra_field' and the annotation
       is not passed to 'word' (w.grouper_of_same_words.grouper_of_same_word_having_this_word.all()':
       if we do: getattr(word, sort) with sort is key inside extra_field ==> No field 
        '''
        st = '<a href="#" onclick="jumpToRow('
        # calculate at which page and row is this word:
        filter_kw = {'{}__lt'.format(sort) : getattr(original_word, sort)} # we can't do getaatr(word, sort) 
        row_id = all_words.filter(**filter_kw).count() # used to get the row in the table
        row_per_page = limit_modif
        page_id = row_id // row_per_page +1
        row_id_inthepage = row_id - row_per_page*(page_id -1)
         
        st += str(page_id)+','+str(row_id_inthepage)+');">'
        en = '</a>'
        return st + word.wordtext + en

    for w in all_words_filtered.prefetch_related('wordtags'): # 'prefetch_related': because it's a m2m relationship
        w_dict = {}
        w_dict['state'] = 'checked' if w.state else '' # checkbox to export to anki
        w_dict['id'] = w.id
        w_dict['status'] = w.status
        w_dict['language_name'] = w.language.name
        w_dict['text_title'] = w.text.title
        w_dict['sentence'] = w.sentence.sentencetext if w.sentence else ''
        w_dict['customsentence'] = w.customsentence if w.customsentence else ''
        w_dict['wordtext'] = w.wordtext if w.wordtext else ''
        w_dict['translation'] = w.translation if w.translation else ''
        w_dict['romanization'] = w.romanization if w.romanization else ''
        w_dict['wordtags'] = [' '+wt.wotagtext for wt in w.wordtags.all()]
        if w.wordtext:
            w_dict['grouper_of_same_words'] = [' '+linked(wo, w) for wo in w.grouper_of_same_words.\
                                                            grouper_of_same_words_for_this_word.all()]
        else:
            w_dict['grouper_of_same_words'] = ''
        if w.compoundword:
            w_dict['compoundword'] = [' '+linked(wo, w) for wo in w.compoundword.\
                                                            compoundwordhavingthiswordinside.all()]
        else:
            w_dict['compoundword'] = ''
        w_dict['modified_date'] ='<span class="hidden">'+ str(w.modified_date.timestamp()) +\
                                '</span>' + str(timesince.timesince(w.modified_date)) 
        if w.extra_field:
            extra_field = json.loads(w.extra_field)
            for extra in extra_field:
                w_dict[list(extra.keys())[0]] = list(extra.values())[0]
        data.append(w_dict)
            
    return JsonResponse({'total': total, 'rows': data}, safe=False)
    
                  
@login_required
@nolang_redirect
def term_list(request):
    ##################################### Display the message (at the rop of the page): default value ###################
    message = None
    noback = None
    errormessage = None
    ######################################## Get Settings ##################################################################
    # get currentlang_id from cookie, else from database
    currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)
    # ... and get the name: used for the page title:
    currentlang_name = getter_settings_cookie_else_db('currentlang_name',request)
    
    ################## LANG FILTERING ######################################################################################
    # get the cookie if set:
    if 'lang' in request.GET.keys(): # the language_list page has a link to display the terms with specific language
        lang_filter_json = '[' + request.GET['lang'] + ']'
        setter_settings_cookie('lang_filter', lang_filter_json, request)
    else:
        lang_filter_json = getter_settings_cookie('lang_filter', request)
        if not lang_filter_json or lang_filter_json == '[]': # first time openin, default it to currentlang
            lang_filter_json = '['+ str(currentlang_id) + ']'
            setter_settings_cookie('lang_filter', lang_filter_json, request)
    lang_filter = json.loads(lang_filter_json)
    lang_filter = [int(i) for i in lang_filter]
    ################## TEXT FILTERING ######################################################################################
    # the text_list page has links to display the words with specific text
    if 'text' in request.GET.keys():
        text_filter_json = '[' + request.GET['text'] + ']'
        setter_settings_cookie('text_filter', text_filter_json, request)
    else: 
        text_filter_json = getter_settings_cookie('text_filter', request)
    text_filter = [] if not text_filter_json else json.loads(text_filter_json)
    text_filter = [int(i) for i in text_filter]
    ################## STATUS FILTERING ######################################################################################
    if 'status' in request.GET.keys():
        status_filter_json = request.GET['status']
        setter_settings_cookie('status_filter', status_filter_json, request)
    else:
        status_filter_json = getter_settings_cookie('status_filter', request)
    status_filter = [] if not status_filter_json else json.loads(status_filter_json)
    status_filter = [int(i) for i in status_filter]

    # get the list of languages to display them in the drop-down menu:
    languages = Languages.objects.filter(owner=request.user).all().order_by('name')
    # the checked checkboxes infulence the list of texts and statuses to display.

    texts = Texts.objects.filter(owner=request.user).order_by('language').all()
    statuses = STATUS_CHOICES

    page_id = 1
    row_id_inthepage = 1
    if request.method == 'GET':
        if 'id' in request.GET.keys():
            wo_id = int(request.GET['id'])
#             order, sort, sort_modif, offset, offset_modif, limit, limit_modif, all_words = requesting_get_by_table(request)
            all_words = Words.objects.exclude(Q(isnotword=True)&Q(isCompoundword=False)).\
                            filter(owner=request.user).\
                                   all()

    total_to_export = Words.objects.filter(owner=request.user, state=True).count()

    # Manage extra field:
    extra_field_json = Words.objects.filter(owner=request.user).values_list('extra_field', flat=True).first()
    if extra_field_json:
        extra_field = json.loads(extra_field_json)
    else:
        extra_field = None

    return render(request, 'lwt/term_list.html',
                   {
                    'languages':languages, 'texts':texts,'statuses':statuses,
                    'currentlang_id':currentlang_id,'currentlang_name':currentlang_name,
                    'lang_filter': lang_filter, 'text_filter': text_filter, 'status_filter': status_filter,
                    'message':message,'errormessage':errormessage,'noback':noback,
                    'total_to_export':total_to_export,
                    'extra_field': extra_field,
                     })