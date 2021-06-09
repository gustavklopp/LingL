# -*- coding: utf-8 -*-
# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template, render_to_string
from django.db.models import F, Q, Value, Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # used for pagination (on text_list for ex.)
from django.http import JsonResponse, HttpResponse #used for ajax
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.http.response import JsonResponse
from django.utils.lorem_ipsum import sentence
# second party
import json
import re
from ast import parse
# local
from lwt.models import *
from lwt.forms import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from lwt.views.text_read import *
from lwt.constants import STATUS_CHOICES
from re import search

''' helper function: called by termform if GET is 'del' 
    it's not 'deleting' the word in the database: it's reinitializing as an unknown word'''
def delete_a_single_word(word):
    word.status=0
    word.translation = None
    word.omanization = None
    word.customsentence = None
    # we give them back the grouper of same words for this word:
    word.grouper_of_same_words = Grouper_of_same_words.objects.get(id=word.id)
    word.compoundword = None
    # ... and delete wordtags too:
    # inside a manytomany relationship:
    # for the wordtag ManyToManyfield
    wordtags_with_this_word = Wordtags.objects.filter(wordtag_with_this_word=word)
    for wordtag in wordtags_with_this_word:
        word.wordtags.remove(wordtag)
    word.save()
    
''' helper function: called by termform if GET is 'del' 
    it's not 'deleting' the word in the database: it's reinitializing as an unknown word'''
def delete_a_compoundword(coword):
    jsonlist = coword.compoundword.wordinside_order
    insidecompoundword_list = json.loads(jsonlist)
    compoundword = coword.compoundword
    for cowo_id in insidecompoundword_list: # delete the FK 
        cowo = Words.objects.get(id=cowo_id)
        cowo.compoundword = None
        cowo.isCompoundword = False
        cowo.show_compoundword = False
        cowo.save()
    compoundword.delete()  # then delete the compoundword in question
    return insidecompoundword_list
    
'''helper func for new_or_edit_word: get the sentence of a word and create curly braces
  around the word in question
    @wo   a word. it can be None if it's called by compoundword (it will defined later then)
    @compoundword_list  it's a list of element inside a compoundword or None if it's called by a Word
    @compoundword_id_list  same than @coumpoundword_list but it has only id number'''
def _create_curlybrace_sentence(wo, compoundword_list=None, compoundword_id_list=None):
    # around compound word elements. the sentence can be got by taking the first element of the compoundwo
    if compoundword_list: 
        wo = compoundword_list[0]
    allword_in_this_sentence = Words.objects.filter(sentence=wo.sentence).\
        exclude(isCompoundword=True, isnotword=True).order_by('order')
    sentenceList = []
    for allword in allword_in_this_sentence:
        # compound word elements
        # TODO looking for similar of compound words???
        if compoundword_list and allword.id in compoundword_id_list: 
            sentenceList.append('**'+allword.wordtext+'**')
        elif not isinstance(wo, list) and allword.wordtext.lower() == wo.wordtext.lower():
            sentenceList.append('**'+allword.wordtext+'**')
        else:
            sentenceList.append(allword.wordtext)
    sentence = ''.join(sentenceList)
    return sentence
    
''' helper function for termform. display the term form at the top right of text_read, 
for a compoundword if a list of compoundword_id is provided, else for a single word '''
def new_or_edit_word(owner, op, compoundword_id_list=None, wo_id=None):

    ########################## Displaying the form for COMPOUNDWORD #########################################
    if compoundword_id_list:
        if len(compoundword_id_list) == 1:
            pass # maybe display an error message because the compoundword has only one element...
        else:
            compoundword_wordtext_list = []
            compoundword_list = []
            compoundword = None # will be defined if it's op=='edit' else if new, it stays None
            for idx in compoundword_id_list:
                wo = Words.objects.get(id=idx)
                compoundword_wordtext_list.append(wo.wordtext)
                compoundword_list.append(wo) 
            dictwebpage_searched_word = ' '.join(compoundword_wordtext_list)

            if op == 'edit':
                # getting the compoundowrd if already defined:
                compoundword = Words.objects.get(wordinside_order=json.dumps(compoundword_id_list, separators=(',',':')))
                f = WordsForm(owner, instance=compoundword)
                customsentence = compoundword.customsentence
            elif op == 'new':
                # the ´instance´ is only used to get the language.id (used inside
                # "manage extra field" link
                f = WordsForm(owner, initial = {'wordinside_order': compoundword_id_list},
                                         instance =  compoundword_list[0])
                customsentence = _create_curlybrace_sentence(compoundword, compoundword_list, compoundword_id_list)
                wo = compoundword_list[0] # used after in the html to search dict at the end of the page

    ########################## Displaying the form for WORD #########################################
    elif wo_id:
        wo = Words.objects.get(id=wo_id)
        # compoundwords:
        compoundword_id_list = [wo.id] # used for after if this word is chosen as the first word of a compoundword
        compoundword_list = [wo] # in the compoundword version, we get only the wordtext, but it's okay...
        dictwebpage_searched_word = wo.wordtext

        f = WordsForm(owner, instance=wo) # put the pre-filled text of the textitem in the field for uwtext

        # displaying the word inside its sentence, with '{' '}' around it:
        customsentence = wo.customsentence
        if op == 'new': 
            customsentence = _create_curlybrace_sentence(wo)

    statuses = STATUS_CHOICES # display radio buttons to choose among available status for a term
#     statuses.pop(0, None) # we dont'need this key (in the form, it always atleast a Learning word)

    if op == 'new': 
        Op_Thing = _('New Term')
        submit_word_button = _('Save')
        submit_singleword_button = ''
    elif op == 'edit':
        Op_Thing = _('Edit Term')
        submit_word_button = _('Change')
        submit_singleword_button = _('Change only this word')
   
    html_ctx ={
                    'form':f, 'wo': wo,'statuses':statuses, 
                    'customsentence':customsentence, 'op': op,
                    # STRING VARIABLES:
                     'Op_Thing': Op_Thing, 'submit_word_button': submit_word_button,
                    'submit_singleword_button': submit_singleword_button,
                    'dictwebpage_searched_word' : dictwebpage_searched_word,
                    # COMPOUNDWORD:
                    'compoundword_id_list': compoundword_id_list, 'compoundword_list': compoundword_list,
        }
    dictwebpage_searched_word = dictwebpage_searched_word
    return html_ctx, dictwebpage_searched_word

'''in topright of text_read, display a list of possible similar words
   the search can be refined with a user-filled searchbox (called by AJAX)
   helper fun for termform()
   @called by: - clicking on new word in text_read section 
              - by doing a search in the termform searchbox ('word' is sent by request.GET)
   @return: list of possible similar words
   '''
def search_possiblesimilarword(request, word=None):
    # search for the already added similar words by the user
    # search with the 3 first letters of the given word. research is made more accurate with the search 
    # box by the user (use in AJAX).
    # we exclude: the same word (of course) (whatever the upper/lowercase) and the already similar word
    
    if word: # clicking on new word in text_read section
        # for longer words, the text we search should be longer. 
        searched_wordtext = word.wordtext[:3]
        if len(word.wordtext) >= 8: 
            searched_wordtext = word.wordtext[:int(round((len(word.wordtext)*2)/3))] # we use 75% of the word similarity in length 
        possiblesimilarword_obj =  Words.objects.\
                filter(Q(language__id=word.language.id)&Q(wordtext__istartswith=searched_wordtext)).\
                       exclude(wordtext__iexact=word.wordtext).\
                       exclude(status=0).\
                       order_by('grouper_of_same_words_id')
    else: # doing a search in the termform searchbox sent by AJAX
        searchboxtext = request.GET['searchboxtext']
        language_id = request.GET['language_id']
        possiblesimilarword_obj =  Words.objects.\
                filter(Q(language__id=language_id)&Q(wordtext__istartswith=searchboxtext[:3])).\
                       exclude(status=0).\
                       order_by('grouper_of_same_words_id')

    possiblesimilarword = possiblesimilarword_obj.values('id','status','sentence','customsentence',
                            'translation','text__title', 'wordtext','grouper_of_same_words_id')
    # If other words have the same FK Grouper_of_same_words, remove them from the list
    possiblesimilarword_distinctFK = [] 
    prev_FK_GOSW_id = -1 # previous foreign key of grouper_of_same_words
    for idx, simword in enumerate(possiblesimilarword):
        if simword['grouper_of_same_words_id'] != prev_FK_GOSW_id:
            possiblesimilarword_distinctFK.append(simword)
            prev_FK_GOSW_id = simword['grouper_of_same_words_id']
        # create the sentence in curly braces:
        if not simword['customsentence']:
            simword['customsentence'] = _create_curlybrace_sentence(possiblesimilarword_obj[idx])
    if word:
        return possiblesimilarword_distinctFK
    else:
        return HttpResponse(json.dumps({'possiblesimilarword':possiblesimilarword_distinctFK}))

    
''' same as above but for compound words
   the search can be refined with a user-filled searchbox (called by AJAX)
   helper fun for termform()
   @called by: - clicking on new word in text_read section
              - by doing a search in the termform searchbox          
   @return: list of possible similar words '''
def search_possiblesimilarCompoundword(request, compoundword_list=None):
    # search for the already added similar words by the user
    # For ex: ver+kaufen will search for a compoundword containing ´ver´ and ´kau´ (in any order)
    # search with the 3 first letters of each of the elements in the coumpound word. 
    # research is made more accurate with the search box by the user (use in AJAX).

    if compoundword_list: # clicking on new word in text_read section
        firstsearch_el = compoundword_list[0].wordtext
        secondsearch_el = compoundword_list[1].wordtext

        possiblesimilarCompoundword =  Words.objects.values('id','sentence','customsentence','translation',
                                            'text__title','wordtext','grouper_of_same_words_id').\
                            filter(Q(language__id=compoundword_list[0].language.id)&\
                                   Q(wordtext__icontains=firstsearch_el[:3])&\
                                   Q(wordtext__icontains=secondsearch_el[:3])).\
                                   exclude(status=0).\
                                   order_by('grouper_of_same_words_id')
    else: # doing a search in the termform searchbox sent by AJAX
        firstsearch_el = request.GET['firstsearch_el']
        secondsearch_el = request.GET['secondsearch_el']
        language_id = request.GET['language_id']

        possiblesimilarCompoundword =  Words.objects.values('id','sentence','customsentence','translation',
                                            'text__title','wordtext','grouper_of_same_words_id').\
                            filter(Q(language__id=language_id)&\
                                   Q(wordtext__icontains=firstsearch_el[:3])&\
                                   Q(wordtext__icontains=secondsearch_el[:3])).\
                                   exclude(status=0).\
                                   order_by('grouper_of_same_words_id')

    # If other words have the same FK Grouper_of_same_words, remove them
    possiblesimilarCompoundword_distinctFK = [] 
    prev_FK_GOSW_id = -1 # previous foreign key of grouper_of_same_words
    for compoundword in possiblesimilarCompoundword:
        if compoundword['grouper_of_same_words_id'] != prev_FK_GOSW_id:
            possiblesimilarCompoundword_distinctFK.append(compoundword)
            prev_FK_GOSW_id = compoundword['grouper_of_same_words_id']

    if compoundword_list:
        return possiblesimilarCompoundword_distinctFK
    else:
        return HttpResponse(json.dumps({'possiblesimilarword':possiblesimilarCompoundword_distinctFK}))

''' helper for termform: superficial copy of a word (or compoundword)
    the boolean return allows to know whether we can do bulk update (forbidden on many2many field) or not'''
def _copy_word(sourceword, destword, save=True):
    destword.status = sourceword.status
    destword.translation = sourceword.translation
    destword.romanization = sourceword.romanization
    destword.customsentence = sourceword.customsentence

    destword.compoundword = sourceword.compoundword
    destword.isCompoundword = sourceword.isCompoundword
    destword.show_compoundword = sourceword.show_compoundword

    # adding a manytomany relationship:
    # for the wordtag ManyToManyfield
    wordtags_with_this_word = Wordtags.objects.filter(wordtag_with_this_word=sourceword)
#     for wordtag in wordtags_with_this_word:
#         destword.wordtags.add(wordtag)
    destword.wordtags.add(*wordtags_with_this_word)

    if save:
        destword.save()    
    
    return False if wordtags_with_this_word else True
    
'''  All similar Words need to be have an updated status also:
             - Those are searching by the same wordtext, OR
             - Those which have already been defined as similar before
                     = i.e they have the same FK Grouper_of_same_words
'''
def get_similar_words_AND_gosw(request, word):
    gosw_to_update = None
    grouper_of_same_words = word.grouper_of_same_words
    if grouper_of_same_words:
        samewordtext_query = Words.objects.filter(language=word.language).\
                             filter(Q(wordtext__iexact=word.wordtext)|\
                                    Q(grouper_of_same_words=grouper_of_same_words))
    else:
        samewordtext_query = Words.objects.filter(language=word.language).\
                                 filter(wordtext__iexact=word.wordtext)

    word_with_gosw_to_update = samewordtext_query.exclude(grouper_of_same_words=None).first()
    if word_with_gosw_to_update:
        gosw_to_update = word_with_gosw_to_update.grouper_of_same_words
        # creating a GOSW if needed
    if not gosw_to_update and samewordtext_query.count() != 1:
        id_string = json.dumps([word.wordtext, word.language.natural_key()])
        gosw_to_update = Grouper_of_same_words.objects.create(id_string=id_string,
                                                               owner=request.user)
    return (samewordtext_query, gosw_to_update)
    
'''    create a http on the topright of text_read with a form to create new term
  called by : - submit button: the AJAX in text_read_clickevent() when clicking on a word
              - click on the ´plus´ because a similar word has been chosen
Call: GET method :
      @op='new' : do insert new (before the form has been posted)
      @op='edit' : do update (before the form has been posted)
      @op='del' : do delete word
      @op='update_status' : do update only the status of the word

Call: POST method:
      @op='new' : do insert new (after the form has been posted)
      @op='edit' : do update (after the form has been posted)
      @op='similar' : do update only the status of the word
'''
def termform(request):
    ###################################################
    #       GET part                                  #
    ###################################################
    if request.method == 'GET':
        # Displaying the form 'newwordform' ################################################### 
        if request.GET['op'] == 'new' or request.GET['op'] == 'edit':# a new word in asked: print the blank form
            op = request.GET['op']
            # Displaying the form for COMPOUNDWORD 
            if 'compoundword_id_list' in request.GET.keys():
                compoundword_id_list = json.loads(request.GET['compoundword_id_list'])
                html_ctx, dictwebpage_searched_word = new_or_edit_word(request.user, op, compoundword_id_list=compoundword_id_list)
            # Displaying the form for WORD 
            else:
                wo_id = int(request.GET['wo_id']) # the text ID
                html_ctx, dictwebpage_searched_word = new_or_edit_word(request.user, op, wo_id=wo_id)

            html = render_to_string('lwt/termform_new_or_edit.html', html_ctx, request)
            
            # Displaying the possible similar words:
            if 'compoundword_id_list' in request.GET.keys():
                possiblesimilarword = search_possiblesimilarCompoundword(request, html_ctx['compoundword_list'])
            else:
                possiblesimilarword = search_possiblesimilarword(request, html_ctx['compoundword_list'][0])

            return HttpResponse(json.dumps({'html':html, 
                                            'dictwebpage_searched_word': dictwebpage_searched_word,
                                            'possiblesimilarword':possiblesimilarword}))

        # delete the word #####################################################################
        if request.GET['op'] == 'del':
            singleword = False
            if 'singleword' in request.GET.keys(): # special case when we want to delete only one word
                singleword = request.GET['singleword']
            wo_id = int(request.GET['wo_id']) 
            word = Words.objects.get(id=wo_id)
            wordtext = word.wordtext
            wostatus = word.status
            sameword_list = []
            sameword_id_list = []
            cowo_id_to_update_in_ajax = []

                
            if singleword:
                delete_a_single_word(word)
                sameword_list.append(word)
                sameword_id_list.append(wo_id)
            elif not singleword:
                words_for_this_grouper_of_same_words = Words.objects.\
                                            filter(grouper_of_same_words=word.grouper_of_same_words)
                for sw in words_for_this_grouper_of_same_words:
                    if not sw.show_compoundword: 
                        delete_a_single_word(sw)
                        sameword_list.append(sw)
                        sameword_id_list.append(sw.id)
                    elif sw.show_compoundword: # the User wants to delete the Compound word
                        insidecompoundword_list = delete_a_compoundword(sw)
                        cowo_id_to_update_in_ajax.extend(insidecompoundword_list) # it produces duplicate (because we add the

            sameword_id_list = list(set(sameword_id_list)) # removing duplicate 
            samewordtextlength = len(sameword_list)
            html = render_to_string('lwt/term_message.html', {'wordtext':wordtext, 'head_message':_('Deleting Term'), 
                                                         'content_message':_('term deleted, now unknown'),
                                                         'sameword_list':sameword_list,'samewordtextlength':samewordtextlength })
            return HttpResponse(json.dumps({'html': html, 
                                            'wowordtext':wordtext, 'wostatus':wostatus,
                                            'iscompoundword': word.isCompoundword,
#                                             'woromanization':word.romanization,
#                                             'cowostatus':word.compoundword.status,
#                                             'cowotranslation': word.compoundword.translation,\
#                                             'coworomanization': word.compoundword.coworomanization,\
                                            'sameword_id_list':sameword_id_list,
                                            'cowo_id_to_update_in_ajax':cowo_id_to_update_in_ajax,
                                            }))
        
        if request.GET['op'] == 'update_status': # make the word 'well-known' or 'ignored'
            sameword_list = []
            sameword_id_list = []

            status_str = request.GET['status'] 
            if status_str == 'wellkwn':
                status = 100
            elif status_str == 'ignored':
                status = 101
            wo_id = request.GET['wo_id']
            word = Words.objects.get(id=wo_id)
#             grouper_of_same_words = word.grouper_of_same_words
#             if grouper_of_same_words:
#                 samewordtext_query = Words.objects.filter(language=word.language).\
#                                             filter(Q(wordtext__iexact=word.wordtext)|\
#                                                    Q(grouper_of_same_words=grouper_of_same_words))
#             else:
#                 samewordtext_query = Words.objects.filter(language=word.language).\
#                                             filter(wordtext__iexact=word.wordtext)
#                 
# 
#             gosw_to_update = samewordtext_query.exclude(grouper_of_same_words=None).first()
#             # creating a GOSW if needed
#             if not gosw_to_update and samewordtext_query.count() != 1:
#                 id_string = json.dumps([word.wordtext, word.language.natural_key()])
#                 gosw_to_update = Grouper_of_same_words.objects.create(id_string=id_string,
#                                                                       owner=request.user)


            samewordtext_query, gosw_to_update = get_similar_words_AND_gosw(request, word)
            for sw in samewordtext_query:
                if gosw_to_update:
                    sw.grouper_of_same_words = gosw_to_update
                sw.status = status
                sameword_list.append(sw)
                sameword_id_list.append(sw.id)
            Words.objects.bulk_update(samewordtext_query, ['grouper_of_same_words', 'status'])

            samewordtextlength = len(sameword_list)
            html = render_to_string('lwt/term_message.html', {'wordtext':word.wordtext, 
                    'head_message':_('Changing Status of "{}"').format(word.wordtext), 
                    'content_message':_('status updated, now : "')+STATUS_CHOICES[status]['name']+'"',
                     'sameword_list':sameword_list, 'samewordtextlength':samewordtextlength }
                                    )
            # used for the hovertooltip 
            if word.isCompoundword:
                cowordtext = word.compoundword.wordtext
                cowostatus = word.compoundword.status
                cowotranslation = word.compoundword.translation
                coworomanization = word.compoundword.romanization
            else:
                cowordtext = cowostatus = cowotranslation = coworomanization = ''
            return HttpResponse(json.dumps({'html': html, 
                                            'wo_id_to_update_in_ajax':sameword_id_list,
                                            'wowordtext':word.wordtext, 'wostatus':status,
                                            'iscompoundword': word.isCompoundword,
                                            'woromanization':word.romanization,
                                            'wotranslation':word.translation,
                                            'cowordtext': cowordtext,
                                            'cowostatus':cowostatus,
                                            'cowotranslation':cowotranslation,
                                            'coworomanization':coworomanization
                                            })
                                )

    ###################################################
    #       POST part                                 #
    ###################################################
    if request.method == 'POST': 
        
        sameword_id_list = []
        sameword_list = []
        samecompoundword_id_list = [] 

        # Case of Posting a similar word:
        if request.POST['op'] == 'similar':
            wo_id = request.POST['wo_id']
            simwo_id = request.POST['simwo_id']

            alreadysavedword = Words.objects.get(id=wo_id)
            simword = Words.objects.get(id=simwo_id)
            simwordtext = simword.wordtext

            # create a gosw if needed:
            gosw = alreadysavedword.grouper_of_same_words
            if not gosw:
                id_string = json.dumps([alreadysavedword.wordtext, alreadysavedword.language.natural_key()])
                gosw = Grouper_of_same_words.objects.create(id_string=id_string,
                                                                       owner=request.user)
                alreadysavedword.grouper_of_same_words = gosw

            sameword_id_list = [simwo_id] # we update the word (the correct color)

            # and update also all the words written similarly than this similar word (you follow? :) 
            samewordtext_query = Words.objects.filter(language=alreadysavedword.language).\
                                 filter(wordtext__iexact=simwordtext)
            for sw in samewordtext_query:
                can_bulkupdate = _copy_word(alreadysavedword, sw, save=False)
                sw.grouper_of_same_words = gosw
                # used in the AJAX to change in realtime the words 
                sameword_id_list.append(sw.id)
                if not can_bulkupdate:
                    sw.save()
            if can_bulkupdate:
                Words.objects.bulk_update(samewordtext_query, ['status','translation','romanization',
                                                           'customsentence','compoundword','isCompoundword',
                                                           'show_compoundword', 'grouper_of_same_words'])

            # Bunch of values more used when creating new word...
            cowo_id_to_update_in_ajax = [] # no need to update other word
            sameword_list = [alreadysavedword] # not sure what this is used for....??? I think it´s only to display
                                    #...the wordtext in fact
            message_wordtext = simword.wordtext
            iscompoundword = False
            cowordtext = cowostatus = coworomanization = cowotranslation = ''
            word = alreadysavedword # this is the name used later...

        else:
        # Case of Posting a new/edit word:
            # it's '{}' (considered as True (Warning!) if not json.loads
            compoundword_id_list_STR = request.POST['compoundword_id_list']
            # for a single word, 'compoundword_id_list_STR = '[8440]' for ex.
            compoundword_id_list = json.loads(compoundword_id_list_STR)
            if 'redefine_only_this_word' in request.POST.keys(): #TODO
                redefine_only_this_word = True
            else:
                redefine_only_this_word = False

            ########################## Processing the form for COMPOUNDWORD #########################################
            if len(compoundword_id_list) > 1:

                # the firstword will be used as reference for copy in the compoundword
                firstword = Words.objects.get(id=compoundword_id_list[0])
                
                f = WordsForm(request.user, json.loads(request.POST['newwordform']), instance=firstword)
                if f.is_valid():
                    compoundword_prototype = f.save(commit=False) 
                    # it's a compound word, so put additional data in word:
                    compoundword = compoundword_prototype
                    compoundword.pk = None
                    
                    compoundword.wordinside_order = json.dumps(compoundword_id_list, separators=(',',':'))
                    compoundword.isCompoundword = True
                    compoundword.isnotword = True #### IMPORTANT!!!!
                    compoundword.save() # you need to save to have a PK (= an id)

                    message_wordtext = [] # used to display the word which haa been updated

                    compoundword_obj_list = []
                    
                    compoundword_wordtext_list = []
                    # and make the words inside the compoundword detectable as such:
                    for idx in compoundword_id_list:
                        wordinside = Words.objects.get(id=idx)
                        wordinside.isCompoundword = True
                        wordinside.compoundword = compoundword # set the ForeignKey
                        wordinside.show_compoundword = True # user can switch that in the clicked tooltip for example
                        compoundword_obj_list.append(wordinside)
                        compoundword_wordtext_list.append(wordinside.wordtext)
                        message_wordtext.append(wordinside.wordtext)
                        samecompoundword_id_list.append(wordinside.id)
                    Words.objects.bulk_update(compoundword_obj_list, ['isCompoundword','compoundword',
                                                                      'show_compoundword'])

                    compoundword.wordtext = '+'.join(compoundword_wordtext_list)
                    wordinside_order_NK = [[wo.wordtext, wo.language.natural_key()]
                                           for wo in compoundword_obj_list]
                    compoundword.wordinside_order_NK = json.dumps(wordinside_order_NK)
                    message_wordtext = compoundword.wordtext
                    cowordtext = compoundword.wordtext
                    
                    compoundword.save()
                    firstword = compoundword_obj_list[0]
                    
                    if redefine_only_this_word: 
                        pass
                    else:
                        # we update by default all the words considered 'similar' by the system 
                        # First, we get the list of sentences where the wordtexts of the compoundword
                        # ...appear simultaneously
                        # I do that to avoid a search in all the sentences: too costy!
                        filter_Q_sentencetext = Q(sentencetext__icontains=compoundword_wordtext_list[0])
                        filter_Q_wordtext = Q(wordtext__iexact=compoundword_wordtext_list[0])
                        for compoundword_wordtext in compoundword_wordtext_list[1:]:
                            args = {'sentencetext__icontains':compoundword_wordtext}
                            filter_Q_sentencetext &= Q(**args)
                            args = {'wordtext__iexact':compoundword_wordtext}
                            filter_Q_wordtext |= Q(**args)
                        sentencesWithSimilarCompoundword = Sentences.objects.\
                                        filter(Q(language=firstword.language)&\
                                                filter_Q_sentencetext).\
                                        exclude(id=firstword.sentence_id)


                        # then we get the Word which correspond to this sentence and which are similar
                        for foundsentence in sentencesWithSimilarCompoundword:
                                
#                             # we create a GOSW (a grouper of same COMPOUND WORD in fact):
#                             id_string = json.dumps([compoundword.wordtext, compoundword.language.natural_key()])
#                             gosw_to_update = Grouper_of_same_words.objects.create(id_string=id_string,
#                                                                                    owner=request.user)

                            cowo_sim_words = Words.objects.filter(
                                                    Q(language=compoundword.language)&\
                                                    Q(sentence=foundsentence)&\
                                                    filter_Q_wordtext)
                            for cowo_sim_el in cowo_sim_words:
                                _copy_word(firstword, cowo_sim_el)
                                samecompoundword_id_list.append(cowo_sim_el.id)

                    word = firstword # used for the hovering tooltip title
                    iscompoundword = True
                    cowostatus = compoundword.status
                    coworomanization = compoundword.romanization
                    cowotranslation = compoundword.translation
                
            ########################## Processing the form for WORD #########################################
            elif len(compoundword_id_list) == 1 or not compoundword_id_list:
                wo_id = request.POST['wo_id']
                virgin_word = Words.objects.get(id=wo_id)
                sameword_list = [virgin_word]
                sameword_id_list = [wo_id]# need to actualize in javascript the wostatus of all these similar words 
                
                f = WordsForm(request.user, json.loads(request.POST['newwordform']), instance=virgin_word)
                if f.is_valid():
                # I need to manually add all the fields, I don't know why??? Bug???
                    word = f.save(commit=False) 
                    word.translation = f.cleaned_data['translation']
                    word.romanization = f.cleaned_data['romanization']
                    word.status = f.cleaned_data['status']
                    word.save()
                    wotagtext_list = [] if f.data["wordtags"] == '' else f.data['wordtags'].split(',')
                    word.wordtags.exclude(wotagtext__in=wotagtext_list).delete() #first, remove non existent tags
                    for wotagtext in wotagtext_list:
                        wordtag = Wordtags.objects.get_or_create( wotagtext=wotagtext)[0]
#                             wordtag = Wordtags.objects.get_or_create(owner=request.user, wotagtext=wotagtext)[0]
                        word.wordtags.add(wordtag)
                    word.save()

                    if redefine_only_this_word:
                        # we give it back its original GOSW
                        word.grouper_of_same_words = Grouper_of_same_words.objects.get(id=word.id)
                        word.save() 
                    
                    else: # we update by default all the words considered 'similar' by the system 
                        # i.e: word that are written similarly 
                        # get the similar words (words that have the same wordtext or that have already been identified as similar)
                        # and update all the other similar words:
                        samewordtext_query, gosw_to_update = get_similar_words_AND_gosw(request, word)

                        for sw in samewordtext_query:
                            if gosw_to_update:
                                sw.grouper_of_same_words = gosw_to_update
                            can_bulkupdate = _copy_word(word, sw, save=False)
                            # used in the AJAX to change in realtime the words 
                            sameword_id_list.append(sw.id)
                            sameword_list.append(sw)
                            if not can_bulkupdate:
                                sw.save()
                        if can_bulkupdate:
                            Words.objects.bulk_update(samewordtext_query, ['status','translation','romanization',
                                                                       'customsentence','compoundword','isCompoundword',
                                                                       'show_compoundword',
                                                                       'grouper_of_same_words'])
                    message_wordtext = word.wordtext

                    iscompoundword = False
                    cowordtext =  cowostatus =  coworomanization =  cowotranslation = ''

        # display the success message
        if request.POST['op'] == 'new':
            head_message= _('   New Term')
            content_message= _('Term saved.') 
        if request.POST['op'] == 'edit':
            head_message= _('   Edit Term')
            content_message= _('Updated.') 
        if request.POST['op'] == 'similar':
            head_message= _('   Word copied from already known word')
            content_message= _(' Considered as a similar word.') 
        samewordtextlength = len(sameword_list)

        wowordtext = word.wordtext
        wostatus = word.status
        wotranslation = word.translation
        woromanization = word.romanization
        show_compoundword = word.show_compoundword

        html = render_to_string('lwt/term_message.html', 
                            {'message_wordtext':message_wordtext, 'head_message':head_message, 
                             'content_message':content_message,
                             'sameword_list': sameword_list,'samewordtextlength':samewordtextlength})
        return HttpResponse(json.dumps({'html':html, 'iscompoundword':iscompoundword, 
            'wowordtext':wowordtext, 'wostatus':wostatus, 'woromanization':woromanization, 
            'wotranslation':wotranslation, 'cowordtext': cowordtext, 'cowostatus':cowostatus, 
            'coworomanization':coworomanization, 'cowotranslation':cowotranslation, 
            'wo_id_to_update_in_ajax':sameword_id_list,
            'cowo_id_to_update_in_ajax': samecompoundword_id_list,
            'show_compoundword': show_compoundword
                                        }))

'''called by lwt/ajax_termform.js/ajax_submit_termformSearchbox
    search other similar word with the input given
    and open a new bottomright dictwebpage '''
def submit_termformSearchbox(request):
    pass #not used finally