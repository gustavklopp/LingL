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
from django.http.response import JsonResponse
from django.utils import timezone, timesince
from django.utils.translation import ugettext as _, ngettext
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.lorem_ipsum import sentence, words
from django.contrib import messages
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


'''use by export2anki_exporter and by selectivebackup_exporter and by term_list
    called by ajax to un/select the rows and save the state in the database'''
def select_rows(request):
    op = request.GET['op']
    check_uncheck = request.GET['check_uncheck']

    warning_deletion = 0

    possible_selected_rows_json = list(Settings_selected_rows.objects.filter(
                        owner=request.user).values_list('possible_selected_rows', flat=True))
    possible_selected_rows_list = json.loads(possible_selected_rows_json[0])

    # clicking on 'check all'
    if op == 'all':
        words_possible_selected_rows = Words.objects.filter(id__in=possible_selected_rows_list)
        # we can't check a word for deletion if it's still linked to a text 
        warning_deletion = words_possible_selected_rows.exclude(text=None).count()
        if not warning_deletion:
            words_possible_selected_rows.update(state=True)
            currently_selected_rows_nb = len(possible_selected_rows_list)
    # clicking on 'uncheck all'
    elif op == 'none':
        Words.objects.filter(id__in=possible_selected_rows_list).update(state=False)
        currently_selected_rows_nb = 0
    # toggle one checkbox of one row (checking or unchecking it)
    else:
        ids = json.loads(op)
        ids = [ids] if not isinstance(ids, list) else ids # it can be a single id or a list of ids
        wos = Words.objects.filter(id__in=ids) #... and id__in : it needs a type list 
        
        # and increase or decrease the total number of selected words (we need to know its amount before)
        # ...and also the current state of the word
        currently_selected_rows_nb = list(Settings_selected_rows_nb.objects.filter(
            owner=request.user).values_list('currently_selected_rows_nb', flat=True))[0]

        for wo in wos:
            if check_uncheck == 'check':
                # we can't check a word for deletion if it's still linked to a text 
                if not wo.text: 
                    wo.state = True
                    currently_selected_rows_nb += 1
                else:
                    warning_deletion += 1
            elif check_uncheck == 'uncheck':
                wo.state = False
                currently_selected_rows_nb -= 1
        Words.objects.bulk_update(wos, ['state'])
        
    # update the total number of selected words
    Settings_selected_rows_nb.objects.filter(
                owner=request.user).update(currently_selected_rows_nb=currently_selected_rows_nb)

    return JsonResponse({'total': currently_selected_rows_nb, 'warning_deletion':warning_deletion}, safe=False)


''''the checkboxes to filter the terms '''
def termlist_filter(request):
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
    
''' called by ajax (built-in function) inside bootstrap-table #word_table to fill the table'''
def load_wordtable(request):
    # func requesting_get_by_table is in lwt/views/_utilities_views.py
    order, sort, sort_modif, offset, offset_modif, limit, limit_modif, all_words = requesting_get_by_table(request, Words)

    if 'search' in request.GET.keys():
        search = request.GET['search']
        if search != '': # when deleting the previous search, ajax will send the search word ''. consider it like No filter
            all_words = all_words.filter(wordtext=search)
    # func list_filtering is in lwt/views/_utilities_views.py

    if not all_words: # no words to display because database is empty
        return JsonResponse({'total': 0, 'rows': []}, safe=False)

    ###########################################
    #    Do the filtering                    #
    ##########################################
    all_words = list_filtering(all_words, request) 
    
    # save the total list of selected item : used when clicking on button 'check/uncheck all'
    currently_selected_rows_nb = all_words.filter(state=True).count()
    Settings_selected_rows_nb.objects.update_or_create(
                                        owner=request.user, 
                                        defaults = {'currently_selected_rows_nb': currently_selected_rows_nb},)
    # and the total list of words in the table 
    possible_selected_rows = json.dumps(list(all_words.values_list('id', flat=True)))
    Settings_selected_rows.objects.update_or_create(
                                        owner=request.user, 
                                        defaults = {'possible_selected_rows': possible_selected_rows},)

    total = all_words.count() 
    
#         lang_id = getter_settings_cookie('term_list_lang_id', request) # return 'None' if not defined
# 
#         if request.method == 'GET' and 'lang_id' in request.GET.keys():
#             lang_id = int(request.GET['lang_id'])
#             request.session['term_list_lang_id'] = lang_id
# 
#         if lang_id: # by defautl. if the lang has been set in the session, filter on this lang
#             all_words = all_words.filter(language__id=lang_id)
    data = []

    all_words_filtered = all_words[offset_modif:offset_modif + limit_modif]

    ''' create a link inside the bootstrap table: clicking on the word jump to the right place 
    we use 'original_word' only to get the annotation if the sorting is on 'extra_field': indeed,
    we have previously annotated 'original_word' with the key form 'extra_field' and the annotation
    is not passed to 'word' (w.grouper_of_same_words.grouper_of_same_word_having_this_word.all()':
    if we do: getattr(word, sort) with sort is key inside extra_field ==> No field 
    NOTE: function 'jumpToRow' is defined in term_list.html
    '''
    def _linked(word, original_word):
        sentence = word.customsentence if word.customsentence else word.sentence.sentencetext
        st = '<a href="#" title="(\''+sentence+'\')" onclick="jumpToRow('
        # calculate at which page and row is this word:
        # we can't do getattr(word, sort) ????
#         filter_kw = {'{}__lt'.format(sort) : getattr(original_word, sort)} 
        filter_kw = {'{}__lt'.format(sort) : getattr(word, sort)} 
        row_id = all_words.filter(**filter_kw).count() # used to get the row in the table
        row_per_page = limit_modif
        page_id = row_id // row_per_page +1
        row_id_inthepage = row_id - row_per_page*(page_id -1)
         
        st += str(page_id)+','+str(row_id_inthepage)+');">'
        en = '</a>'
        return st + word.wordtext + en

    '''use inside the word_table cells to truncate the too big text and display "more"'''
    def _truncate(text, maxtext=50):
        if len(text) > maxtext:
            not_trunc_text = '<span hidden>{}<span class="d-inline btn btn-link" '+\
                            'onclick="$(this).parent().next().prop(\'hidden\',false);'+\
                            '$(this).parent().prop(\'hidden\',true);"> '+_('hide')+\
                            '</span></span>'
            trunc_text = '<span>{}...<span class="d-inline btn btn-link" '+\
                'onclick="$(this).parent().prev().prop(\'hidden\',false);'+\
              '$(this).parent().prop(\'hidden\',true);">'+_('more')+\
              '</span><span>'
            return not_trunc_text.format(text) + trunc_text.format(text[:maxtext])
        else:
            return text

#     for w in all_words_filtered.prefetch_related('wordtags'): # 'prefetch_related': because it's a m2m relationship
    for w in all_words_filtered: # 'prefetch_related': because it's a m2m relationship
        w_dict = {}
        w_dict['state'] = 'checked' if w.state else '' # checkbox to export to anki
        w_dict['id'] = w.id
        # the 'hidden' part in 'status' allows to color the row accordingly in the html file
        w_dict['status'] = '<span hidden>{:03d}</span>'.format(w.status)+\
                                get_name_status(w.status)+'<small>['+str(w.status)+']</small>'
        w_dict['language_name'] = w.language.name
        w_dict['text_title'] = w.text.title if w.text else ''
        sentence = w.sentence.sentencetext if w.sentence else ''
        w_dict['sentence'] = _truncate(sentence)
        customsentence = w.customsentence if w.customsentence else ''
        w_dict['customsentence'] = _truncate(customsentence)
        w_dict['wordtext'] = w.wordtext if w.wordtext else ''
        w_dict['translation'] = w.translation if w.translation else ''
        w_dict['romanization'] = w.romanization if w.romanization else ''
        w_dict['wordtags'] = [' '+wt.wotagtext for wt in w.wordtags.all()]
        if w.grouper_of_same_words:
            w_dict['grouper_of_same_words'] = [' '+_linked(wo, w) for wo in w.grouper_of_same_words.\
                                                            grouper_of_same_words_for_this_word.all()]
        else:
            w_dict['grouper_of_same_words'] = ''
        if w.compoundword:
            w_dict['compoundword'] = [' '+_linked(wo, w) for wo in w.compoundword.\
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

    # deleting word(s)
    if request.method == 'POST':
        possible_selected_rows_json = list(Settings_selected_rows.objects.filter(
                owner=request.user).values_list('possible_selected_rows', flat=True))[0]
        possible_selected_rows_ids = json.loads(possible_selected_rows_json)
        deleted_wo_nb = Words.objects.filter(Q(id__in=possible_selected_rows_ids)&\
                                                Q(state=True)).delete()[0]

        # and update the Settings_selected_rows and Settings_selected_rows_nb:
        words_with_state_True = 0
        Settings_selected_rows_nb.objects.filter(owner=request.user).update(
                                        currently_selected_rows_nb=words_with_state_True)
        
        # the remaining words of the 'possible_selected_rows_ids'
        remaining_words = Words.objects.filter(id__in=possible_selected_rows_ids)
        possible_selected_row = json.dumps(list(remaining_words.values_list('id', flat=True)))
        Settings_selected_rows.objects.filter(owner=request.user).update(possible_selected_rows=possible_selected_row)
        
        delwo_message = ngettext('%(count)d word successfully deleted.', '%(count)d words successfully deleted',
                                deleted_wo_nb ) % {'count': deleted_wo_nb }
        messages.add_message(request, messages.SUCCESS, delwo_message)
        
        # update database also
        set_word_database_size(request)

    else:
        # Get the total count of currently selected words (used to display: "XXX words to delete"
        # i.e the words with state == True
        words_with_state_True = list(Settings_selected_rows_nb.objects.filter(
                    owner=request.user).values_list('currently_selected_rows_nb', flat=True))
        words_with_state_True = 0 if not words_with_state_True else words_with_state_True[0]

    # Display the message (at the rop of the page): default value 
    noback = None # Is it useful???
    ######################################## Get Settings ##################################################################
    # get currentlang_id from cookie, else from database
    currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)
    # ... and get the name: used for the page title:
    currentlang_name = getter_settings_cookie_else_db('currentlang_name',request)
    
    ######################################################################################################
    # Create the checkboxes at the top. The actual filtering of the Words is done in load_wordtable()    #
    ######################################################################################################

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
    ################## WORDTAG FILTERING ######################################################################################
    wordtag_filter_json = getter_settings_cookie('wordtag_filter', request)
    wordtag_filter = [] if not wordtag_filter_json else json.loads(wordtag_filter_json)
    wordtag_filter = [int(i) for i in wordtag_filter]
    wordtags = Wordtags.objects.filter(owner=request.user).all().order_by('wotagtext')
    # creating the wordtags_list
    wordtags_list = []
    wordtags_list_empty = True
    for wordtag in wordtags:
        # get the languages which are found associated to this wordtag
        wordtag_lang = Words.objects.filter(wordtags=wordtag).values_list('language_id', flat=True).all()
        if set(wordtag_lang).isdisjoint(set(lang_filter)): # some languages are common
            wordtags_list.append({'tag':wordtag, 'bold': True, 'lang': list(wordtag_lang)})
        else:
            wordtags_list.append({'tag':wordtag, 'bold': False, 'lang': list(wordtag_lang)})
            wordtags_list_empty = False

    ################## COMPOUNDWORD FILTERING ######################################################################################
    compoundword_filter_json = getter_settings_cookie('compoundword_filter', request)
    compoundword_filter = [] if not compoundword_filter_json else json.loads(compoundword_filter_json)
    compoundword_filter = [str_to_bool(i) for i in compoundword_filter]
    isCompoundword_textIds = list(Words.objects.filter(Q(owner=request.user)&Q(isCompoundword=True)).values_list(
                                                    'id', flat=True))
    isnotCompoundword_textIds = list(Words.objects.filter(Q(owner=request.user)&Q(isCompoundword=False)).values_list(
                                                    'id', flat=True))

    compoundword_textIds_boldlist = [ {'isCompoundword':False, 
                                       'txt_set':json.dumps(isnotCompoundword_textIds)},
                    {'isCompoundword':True, 'txt_set':json.dumps(isCompoundword_textIds)}]

    ####################################################################################################
    # get the list of languages to display them in the drop-down menu:
    languages = Languages.objects.filter(owner=request.user).all().order_by('name')
    # the checked checkboxes infulence the list of texts and statuses to display.

    texts = Texts.objects.filter(owner=request.user).order_by('language').all()

    # Manage extra field:
    extra_field_json = Words.objects.filter(owner=request.user).values_list('extra_field', flat=True).first()
    if extra_field_json:
        extra_field = json.loads(extra_field_json)
    else:
        extra_field = None
    
    # get the current database size:
    database_size = get_word_database_size(request)

    return render(request, 'lwt/term_list.html',
                   {'languages':languages, 'texts':texts,'statuses':STATUS_CHOICES,
                    'currentlang_id':currentlang_id,'currentlang_name':currentlang_name,

                    'lang_filter': lang_filter, 
                    'text_filter': text_filter, 
                    'status_filter': status_filter,
                    'wordtag_filter': wordtag_filter, 'wordtags_list':wordtags_list, 'wordtags_list_empty':wordtags_list_empty,
                    'compoundword_filter':compoundword_filter, 'compoundword_textIds_boldlist':compoundword_textIds_boldlist,

                    'noback':noback,
                    'words_with_state_True':words_with_state_True,
                    'extra_field': extra_field,
                     'database_size':database_size})
    