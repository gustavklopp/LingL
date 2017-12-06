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


                  
def delete_a_single_word(word):
    ''' helper function: called by termform if GET is 'del' '''
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
    
def copy_a_word_to_a_simword(word, simword):
    ''' helper function: called by term detail if POST.
    update the similar words using the 'word': copying its data '''
    simword.grouper_of_same_words = word.grouper_of_same_words # give them the same grouper than the original word (useful only for the word with the same wordtext)
    simword.compoundword = word.compoundword
    simword.status = word.status
    simword.translation = word.translation
    simword.romanization = word.romanization
    simword.customsentence = word.customsentence
    # adding a manytomany relationship:
    # for the wordtag ManyToManyfield
    wordtags_with_this_word = Wordtags.objects.filter(wordtag_with_this_word=word)
    for wordtag in wordtags_with_this_word:
        simword.wordtags = wordtag
    simword.save()
    
def new_or_edit_word(op, compoundword_id_list=None, wo_id=None):
    ''' helper function for termform. display the term form at the top right of text_read, 
    for a compoundword if a list of compoundword_id is provided, else for a single word '''

    ########################## Displaying the form for COMPOUNDWORD #########################################
    if compoundword_id_list:
        if len(compoundword_id_list) == 1:
            pass # maybe display an error message because the compoundword has only one element...
        else:
            if op == 'edit':
                # getting the compoundowrd if already defined:
                compoundword = Words.objects.get(wordinside_order=json.dumps(compoundword_id_list, separators=(',',':')))
                f = WordsForm(instance=compoundword)
                customsentence = compoundword.customsentence
            elif op == 'new':
                f = WordsForm(initial = {'wordinside_order': compoundword_id_list})
                customsentence = ''

            # displaying the word inside its sentence, with '{' '}' around it:
            if not customsentence: 
                #the sentences are displayed only if it's empty or null. else, it means that
                # the user has already defined a custom sentence. Leave it!
                # Get the sentence by finding where one of the word inside is.
                firstword = Words.objects.get(id=compoundword_id_list[0])
                wo = firstword # used after in the html to search dict at the end of the page
                allword_in_this_sentence = Words.objects.filter(sentence=firstword.sentence).\
                    exclude(isCompoundword=True,isnotword=True).order_by('order')
                sentenceList = []
                for allword in allword_in_this_sentence:
                    if allword.id in compoundword_id_list:
                        sentenceList.append('{'+allword.wordtext+'}')
                    else:
                        sentenceList.append(allword.wordtext)
                customsentence = ''.join(sentenceList)
            compoundword_list = []
            for idx in compoundword_id_list:
                compoundword_list.append(Words.objects.values_list('wordtext',flat=True).\
                                            get(id=idx)) 
            dictwebpage_searched_word = ' '.join(compoundword_list)
    ########################## Displaying the form for WORD #########################################
    elif wo_id:
        wo = Words.objects.get(id=wo_id)
        # compoundwords:
        compoundword_id_list = [wo.id] # used for after if this word is chosen as the first word of a compoundword
        compoundword_list = [wo] # in the compoundword version, we get only the wordtext, but it's okay...
        dictwebpage_searched_word = wo.wordtext

        f = WordsForm(instance=wo) # put the pre-filled text of the textitem in the field for uwtext

        # displaying the word inside its sentence, with '{' '}' around it:
        customsentence = wo.customsentence
        if not customsentence: 
            #the sentences are displayed only if it's empty or null. else, it means that
            # the user has already defined a custom sentence. Leave it!
            allword_in_this_sentence = Words.objects.filter(sentence=wo.sentence).\
                    exclude(isCompoundword=True,isnotword=True).order_by('order')
            sentenceList = []
            for allword in allword_in_this_sentence:
                if allword == wo:
                    sentenceList.append('{'+allword.wordtext+'}')
                else:
                    sentenceList.append(allword.wordtext)
            customsentence = ''.join(sentenceList)

    statuses = get_statuses() # display radio buttons to choose among available status for a term
    del statuses[0] # we dont'need this key (in the form, it always atleast a Learning word)

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

def termform(request):
    ''' called by the AJAX in text_read_clickevent() when clicking on a word
    create a http on the topright of text_read with a form to create new term
/**************************************************************
'new' word.id

Call: GET method ?....
      ... op=new ... do insert new (before the form has been posted)
      ... op=edit ... do update (before the form has been posted)
      ... op=del ... do delete word
      ... op=update_status ... do update only the status of the word
Call: POST method ?....
      ... op=new ... do insert new (after the form has been posted)
      ... op=edit ... do update (after the form has been posted)
***************************************************************/
    '''
    if request.method == 'GET':

        # Displaying the form 'newwordform' 
        if request.GET['op'] == 'new' or request.GET['op'] == 'edit':# a new word in asked: print the blank form
            op = request.GET['op']
            # Displaying the form for COMPOUNDWORD 
            if 'compoundword_id_list' in request.GET.keys():
                compoundword_id_list = json.loads(request.GET['compoundword_id_list'])
                html_ctx, dictwebpage_searched_word = new_or_edit_word(op, compoundword_id_list=compoundword_id_list)
            # Displaying the form for WORD 
            else:
                wo_id = int(request.GET['wo_id']) # the text ID
                html_ctx, dictwebpage_searched_word = new_or_edit_word(op, wo_id=wo_id)

            html = render_to_string('lwt/termform_new_or_edit.html', html_ctx, request)
            return HttpResponse(json.dumps({'html':html, 'dictwebpage_searched_word': dictwebpage_searched_word}))
#             return render(request, 'lwt/termform_new_or_edit.html', ctx)

        #################### delete the word #####################################################################
        if request.GET['op'] == 'del':
            singleword = False
            if 'singleword' in request.GET.keys(): # special case when we want to delete only one word
                singleword = request.GET['singleword']
            wo_id = int(request.GET['wo_id']) 
            word = Words.objects.get(id=wo_id)
            wordtext = word.wordtext
            wostatus = word.status
            samewordtext = []
            wo_id_to_update_in_ajax = []
            cowo_id_to_update_in_ajax = []

                
            if singleword:
                delete_a_single_word(word)
                samewordtext.append(word)
                wo_id_to_update_in_ajax.append(wo_id)
            elif not singleword:
                words_for_this_grouper_of_same_words = Words.objects.\
                                            filter(grouper_of_same_words=word.grouper_of_same_words)
                for sw in words_for_this_grouper_of_same_words:
                    if not sw.show_compoundword: 
                        delete_a_single_word(sw)
                        samewordtext.append(sw)
                        wo_id_to_update_in_ajax.append(sw.id)
                    elif sw.show_compoundword: # the User wants to delete the Compound word
                        insidecompoundword_list = delete_a_compoundword(sw)
                        cowo_id_to_update_in_ajax.extend(insidecompoundword_list) # it produces duplicate (because we add the

            wo_id_to_update_in_ajax = list(set(wo_id_to_update_in_ajax)) # removing duplicate 
            samewordtextlength = len(samewordtext)
            html = render_to_string('lwt/term_message.html', {'wordtext':wordtext, 'head_message':_('Deleting Term'), 
                                                         'content_message':_('term deleted, now unknown'),
                                                         'samewordtext':samewordtext,'samewordtextlength':samewordtextlength })
            return HttpResponse(json.dumps({'html': html, 
                                            'wowordtext':wordtext, 'wostatus':wostatus,
                                            'iscompoundword': word.isCompoundword,
#                                             'woromanization':word.romanization,
#                                             'cowostatus':word.compoundword.status,
#                                             'cowotranslation': word.compoundword.translation,\
#                                             'coworomanization': word.compoundword.coworomanization,\
                                            'wo_id_to_update_in_ajax':wo_id_to_update_in_ajax,
                                            'cowo_id_to_update_in_ajax':cowo_id_to_update_in_ajax,
                                            }))
        
        if request.GET['op'] == 'update_status': # make the word 'well=known' or 'ignored'
            status = request.GET['status']
            wo_id = request.GET['wo_id']
            word = Words.objects.get(id=wo_id)
            # get the similar words (words that have the same wordtext or that have already been identified as similar)
            grouper_of_same_words = word.grouper_of_same_words
            samewordtext_query = Words.objects.filter(language=word.language).filter(Q(wordtext=word.wordtext)|\
                                    Q(grouper_of_same_words=grouper_of_same_words))
            samewordtext = []
            wo_id_to_update_in_ajax = []
            for sw in samewordtext_query:
                if status == 'wellkwn':
                    sw.status = 100
                if status == 'ignored':
                    sw.status = 101
                sw.grouper_of_same_words = grouper_of_same_words
                sw.save()
                samewordtext.append(sw)
                wo_id_to_update_in_ajax.append(sw.id)
            samewordtextlength = len(samewordtext)
            html = render_to_string('lwt/term_message.html', {'wordtext':word.wordtext, 'head_message':_('Changing Status'), 
                                                         'content_message':_('status updated, now ') + status,
                                                         'samewordtext':samewordtext,'samewordtextlength':samewordtextlength })
            return HttpResponse(json.dumps({'html': html, 'wowordtext':word.wordtext, 'wo_id_to_update_in_ajax':wo_id_to_update_in_ajax}))

    ################################# the form has been posted #############################################################
    if request.method == 'POST': 
        # it's '{}' (considered as True (Warning!) if not json.loads
        compoundword_id_list_STR = request.POST['compoundword_id_list']
        compoundword_id_list_OBJ = json.loads(compoundword_id_list_STR)
        if 'redefine_only_this_word' in request.POST.keys():
            redefine_only_this_word = True
        else:
            redefine_only_this_word = False
        ########################## Processing the form for COMPOUNDWORD #########################################
        if len(compoundword_id_list_OBJ) > 1:

            # the firstword will be used as reference for copy in the compoundword
            firstword = Words.objects.get(id=compoundword_id_list_OBJ[0])
            # and the other will be copy on
            cowo_id_to_update_in_ajax = compoundword_id_list_OBJ
            
            chosen_similarword_wo_id = json.loads(request.POST['chosen_similarword']) # get the list of the words id that the user want to update because "similar"
            chosen_similarword = [Words.objects.get(id=simwo_id) for simwo_id in chosen_similarword_wo_id]

            f = WordsForm(json.loads(request.POST['newwordform']))
            if f.is_valid():
                compoundword = f.save() 
                # it's a compound word, so put additional data in word:
                compoundword.owner = request.user
                compoundword.language = firstword.language
                compoundword.sentence = firstword.sentence
                compoundword.text = firstword.text
                compoundword.wordinside_order = json.dumps(compoundword_id_list_OBJ, separators=(',',':'))
                compoundword.isCompoundword = True
                compoundword.isnotword = True
                compoundword.save()
                # give it a grouper_of_same_word FK with the same id:
                grouper_of_same_words = Grouper_of_same_words.objects.create(id=compoundword.id)
                compoundword.grouper_of_same_words = grouper_of_same_words
                compoundword.save()

                message_wordtext = [] # used to display the word which haa been updated
                # and make the words inside the compoundword detectable as such:
                for idx in compoundword_id_list_OBJ:
                    wordinside = Words.objects.get(id=idx)
                    wordinside.isCompoundword = True
                    wordinside.compoundword = compoundword # set the ForeignKey
                    wordinside.show_compoundword = True # user can switch that in the clicked tooltip for example
                    wordinside.save()
                    message_wordtext.append(wordinside.wordtext)
                
                # TODO: it's not words written similarly, it's same regex pattern with the wordinside
                samewordtext = []
                wo_id_to_update_in_ajax = [] # need to actualize in javascript the wostatus of all these similar words 
#                     samewordtext = [word]
#                     wo_id_to_update_in_ajax = [word.id] # need to actualize in javascript the wostatus of all these similar words 
                
                if redefine_only_this_word:
                    pass
                    # we give it back its original GOSW
#                         word.grouper_of_same_words = Grouper_of_same_words.objects.get(id=word.id)
#                         word.save() 
                
                if chosen_similarword: # we need to update words considered similar by the user 
                    pass
#                         for sw in chosen_similarword:
#                             copy_a_word_to_a_simword(word, sw)
#                             samewordtext.append(sw)
#                             wo_id_to_update_in_ajax.append(sw.id)

                if not redefine_only_this_word: # we update by default all the words considered 'similar' by the system 
                    pass
                    # i.e: word that are written similarly 
                    # get the same compound word by regex (words that have the same wordtext or that have already been identified as similar)
#                         grouper_of_same_words = word.grouper_of_same_words
#                         samewordtext_query = Words.objects.filter(language=wo.language).filter(Q(wordtext=wo.wordtext)|\
#                                                 Q(grouper_of_same_words=grouper_of_same_words)).exclude(id=wo_id)
#                         # and update all the other similar words:
#                         for sw in samewordtext_query:
#                             copy_a_word_to_a_simword(word, sw)
#                             wo_id_to_update_in_ajax.append(sw.id)
#                             samewordtext.append(sw)
                word = firstword # used for the hovering tooltip title
                iscompoundword = True
                cowostatus = compoundword.status
                coworomanization = compoundword.romanization
                cowotranslation = compoundword.translation
                message_wordtext = '+'.join(message_wordtext)
            
        ########################## Processing the form for WORD #########################################
        elif len(compoundword_id_list_OBJ) == 1:
            wo_id = request.POST['wo_id']
            virgin_word = Words.objects.get(id=wo_id)
            samewordtext = [virgin_word]
            wo_id_to_update_in_ajax = [wo_id]# need to actualize in javascript the wostatus of all these similar words 
            
            
            chosen_similarword_wo_id = json.loads(request.POST['chosen_similarword'])
            chosen_similarword = [Words.objects.get(id=simwo_id) for simwo_id in chosen_similarword_wo_id]

            f = WordsForm(json.loads(request.POST['newwordform']), instance=virgin_word)
            if f.is_valid():
                word = f.save() 
                
                if redefine_only_this_word:
                    # we give it back its original GOSW
                    word.grouper_of_same_words = Grouper_of_same_words.objects.get(id=word.id)
                    word.save() 
                
                if chosen_similarword: # we need to update words considered similar by the user 
                    for sw in chosen_similarword:
                        copy_a_word_to_a_simword(word, sw)
                        samewordtext.append(sw)
                        wo_id_to_update_in_ajax.append(sw.id)

                if not redefine_only_this_word: # we update by default all the words considered 'similar' by the system 
                    # i.e: word that are written similarly 
                    # get the similar words (words that have the same wordtext or that have already been identified as similar)
                    grouper_of_same_words = word.grouper_of_same_words
                    samewordtext_query = Words.objects.filter(language=word.language).filter(Q(wordtext=word.wordtext)|\
                                            Q(grouper_of_same_words=grouper_of_same_words)).exclude(id=wo_id)
                    # and update all the other similar words:
                    for sw in samewordtext_query:
                        copy_a_word_to_a_simword(word, sw)
                        wo_id_to_update_in_ajax.append(sw.id)
                        samewordtext.append(sw)
                cowo_id_to_update_in_ajax = [] 
                message_wordtext = word.wordtext

                iscompoundword = False
                cowostatus = ''
                coworomanization = ''
                cowotranslation = ''

        # display the success message
        if request.POST['op'] == 'new':
            head_message= _('New Term')
            content_message= _('Term saved.') 
        if request.POST['op'] == 'edit':
            head_message= _('Edit Term')
            content_message= _('Updated.') 
        samewordtextlength = len(samewordtext)

        wowordtext = word.wordtext
        wostatus = word.status
        wotranslation = word.translation
        woromanization = word.romanization

        html = render_to_string('lwt/term_message.html', {'message_wordtext':message_wordtext, 'head_message':head_message, 
                                                         'content_message':content_message,
                                                         'samewordtext': samewordtext,'samewordtextlength':samewordtextlength})
        return HttpResponse(json.dumps({'html':html, 
                            'iscompoundword':iscompoundword, 'wowordtext':wowordtext, 
                            'wostatus':wostatus, 'woromanization':woromanization, 'wotranslation':wotranslation, 
                            'cowostatus':cowostatus, 'coworomanization':coworomanization, 'cowotranslation':cowotranslation, 
                            'wo_id_to_update_in_ajax':wo_id_to_update_in_ajax,
                            'cowo_id_to_update_in_ajax': cowo_id_to_update_in_ajax,
                                        }))

            