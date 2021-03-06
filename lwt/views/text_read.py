# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db import transaction
from django.db.models import Q
from django.templatetags.i18n import language
from django.http.response import JsonResponse
from django.http import JsonResponse, HttpResponse #used for ajax
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# second party:
import json
import datetime
# third party
# local
from lwt.models import *
# helper functions:
from lwt.views._nolang_redirect_decorator import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from lwt.views.termform import *

@login_required
@nolang_redirect
def text_read(request,text_id):
    ''' display the text to be read, with lots of javascript...'''
    text = Texts.objects.get(id=text_id)
    # Saving the timestamp for text opening: used after to get the last open texts.
    text.lastopentime = timezone.now()  
    text.save()

    word_inthistext = Words.objects.filter(text=text).order_by('sentence_id', 'order')
    
    # increasing the Learning status: Each time the file is open/window refreshed, we calculate whether it
    # was modified more than 12 hours ago. If yes, update +1 for all word/grouperofsameword/similarword
    # with the basal status of '1' to +1. Max level is '100'.
    time_from_modif = timezone.now() - text.modified_date
#     if time_from_modif > datetime.timedelta(days=1):
    if time_from_modif > datetime.timedelta(hours=24):
        learning_inthistext_groupers = Grouper_of_same_words.objects.filter(
           Q(grouper_of_same_words_for_this_word__text=text )&
           Q(grouper_of_same_words_for_this_word__status__gte=1)).all()
        learning_inthistext_words = Words.objects.filter(grouper_of_same_words__in=learning_inthistext_groupers)
        for wo in learning_inthistext_words:
            wo.status = wo.status + 1 if wo.status + 1 < 100 else 100 # 100 is the status max
            wo.save()
    
    # calculate the statistic (it's the same stats than in text_list)s
    texttotalword = Words.objects.filter(text=text,isnotword=False).count()
    textsavedword = Words.objects.filter(text=text,isnotword=False,status__gt=0).count()
    textwordcount = texttotalword
    textworkcount = textsavedword
    
    # to have the tooltip displayed. Creating the block of text which the Javascript aill read:
    statuses = json.dumps(get_statuses()) # function in _utilities_views
    wordtags = json.dumps(list(Wordtags.objects.values_list('wotagtext',flat=True).order_by('wotagtext')))
    texttags = json.dumps(list(Texttags.objects.values_list('txtagtext',flat=True).order_by('txtagtext')))

    # link to next/previous texts if exists:
    nexttext = Texts.objects.filter(owner=request.user, lastopentime__gt=text.lastopentime).\
                            order_by('-lastopentime').first()
    previoustext = Texts.objects.filter(owner=request.user, lastopentime__lt=text.lastopentime).\
                            order_by('-lastopentime').first()

    return render(request, 'lwt/text_read.html',{ 
                'text':text,
                'previoustext':previoustext,'nexttext':nexttext,
                'textwordcount':textwordcount,'textworkcount':textworkcount,
                # inside thetext div:
                'word_inthistext':word_inthistext,
                # for tooltip
                'statuses':statuses,'wordtags':wordtags,'texttags':texttags,
        })

def dictwebpage(request):
    ''' create dictionary webpage.
    Adapted from: makeOpenDictStrJS(createTheDictLink($wb1,$word)) '''
    # case 1:  AJAX has fetched the JSON on the wwww, then the JSON obj from the www is sent to the view dictwebpage which processes it and 
    # and sends back html.
    if 'json_obj' in request.GET.keys():
        parsed_json_obj = json.loads(request.GET['json_obj'])
        return render(request, 'lwt/_glosbe_api.html', {'result': parsed_json_obj}) 
    # case 2:  AJAX sends the link to process to the view dictwebpage, and the view sends backs a JSON containing the string URL. <iframe> displays it then.  
    else:
        word = request.GET['word']
        wbl = request.GET['wbl']
        # case where it's a lookup sentence:
        if 'issentence' in request.GET.keys() and request.GET['issentence'] != '': # no key "issentence" is sent if the value of 'issentence' is empty in AJAX
            wo_id = int(request.GET['issentence'])
            word = Sentences.objects.values_list('sentencetext',flat=True).get(sentence_having_this_word=wo_id)
        finalurl = createTheDictLink(wbl,word) # create the url of the dictionary, integrating the searched word
        return HttpResponse(json.dumps(finalurl)) 

def show_sentence(request):
    ''' called by AJAX by the form in text_read: shows a list of sentences where the term appears '''
    wo_ids = request.GET['wo_ids']
    wo_ids = json.loads(wo_ids)
    wo_wordtexts = []
    # if compoundword, they must be present in the same sentence, but order is not important here.
    sentences_with_the_same_wordtext = Sentences.objects.all().order_by('sentencetext')
    for idx, wo_id in enumerate(wo_ids):
        word = Words.objects.get(id=wo_id)
        wordtext = word.wordtext
        wo_wordtexts.append(wordtext)
        sentences_with_the_same_wordtext = sentences_with_the_same_wordtext.filter(language=word.language).\
                    filter(sentence_having_this_word__wordtext=wordtext)
    display_sentences_with_the_same_wordtext = []
    # display the little '{' '}' around the words
    for sentence_with_the_same_wordtext in sentences_with_the_same_wordtext: # loop over the sentences
        # get all the words inside this sentence:
        words_in_this_sentence = Words.objects.filter(sentence=sentence_with_the_same_wordtext).all().order_by('order')
        sentenceList = []
        for wo in words_in_this_sentence: #  loop inside the sentence: replace the 'word' by '{word}' (that's cooler!)
            if wo.wordtext in wo_wordtexts:
                sentenceList.append('{'+wo.wordtext+'}')
            else:
                sentenceList.append(wo.wordtext)
        display_sentences_with_the_same_wordtext.append(''.join(sentenceList))
    sentences_for_json = list(zip(sentences_with_the_same_wordtext.\
                                        values_list('text__id','text__title'),\
                                 display_sentences_with_the_same_wordtext))
    sentences_json = json.dumps(sentences_for_json)
    return JsonResponse(sentences_json, safe=False)

def search_possiblesimilarword(request): 
    ''' called by AJAX by the form in text_read: shows a list of words, similar to the given word ''' 
    wo_id = request.GET['wo_id']
    word = Words.objects.get(id=wo_id)
    searchboxtext = request.GET['searchboxtext']
    # search with the 3 first letters of the given word. research is made more accurate with the search box by the user.
    # we exclude: the same word (of course) and the already similar word
    possible_similarword = Words.objects.values('id','text__title','wordtext','status').\
                        filter(Q(language__id=word.language.id)&Q(wordtext__istartswith=word.wordtext[:3])&\
                               Q(wordtext__istartswith=searchboxtext)).\
                               exclude(grouper_of_same_words=word.grouper_of_same_words).\
                               exclude(wordtext=word.wordtext).\
                               order_by('wordtext')
    # search for the already added similar words by the user
    alreadyadded_similarword =  Words.objects.values('id','text__title','wordtext').\
                               filter(grouper_of_same_words=word.grouper_of_same_words).\
                               exclude(wordtext=word.wordtext).\
                               order_by('wordtext')
    search_similarword_json = json.dumps({'possible_similarword':list( possible_similarword),
                                          'alreadyadded_similarword': list(alreadyadded_similarword)})
    return JsonResponse(search_similarword_json, safe=False)

def create_or_del_similarword(request):
    ''' called by AJAX by the form in termform: 
    - a word is consideted as similar: copy the data from the word to the similar one (and use a Grouper.
    - undoing this: delete the similar word '''
    op = request.GET['op']
    simwo_id = request.GET['simwo_id']
    wo_id = request.GET['wo_id']
    word = Words.objects.get(id=wo_id)
    similarword = Words.objects.get(id=simwo_id)
    similarwords = Words.objects.filter(grouper_of_same_words=similarword.grouper_of_same_words)

    if op == 'create': # creating the similar word
        grouper_of_same_words = word.grouper_of_same_words
        # and put all the same data in both words: (copy data from word -> similarword)
        for sw in similarwords:
            sw.grouper_of_same_words = grouper_of_same_words
            sw.status = word.status
            sw.customsentence = word.customsentence
            sw.translation = word.translation
            sw.romanization = word.romanization
            # ... and copy wordtags too:
            # adding a manytomany relationship:
            # for the wordtag ManyToManyfield
            wordtags_with_this_word = Wordtags.objects.filter(wordtag_with_this_word=word)
            for wordtag in wordtags_with_this_word:
                similarword.wordtags = wordtag
            sw.save()
        
        return HttpResponse(json.dumps({'simwo_id':simwo_id, 'simwotranslation':similarword.translation,
                                        'simworomanization':similarword.romanization,'simwostatus':similarword.status})) 
    elif op == 'del': # deleting the similar word
        for sw in similarwords:
            sw.status=0
            sw.translation = None
            sw.omanization = None
            sw.customsentence = None
            # and give them back a grouper original (the one with the same id than their one)
            sw.grouper_of_same_words = Grouper_of_same_words.objects.get(id=sw.id)
            # ... and delete wordtags too:
            # inside a manytomany relationship:
            # for the wordtag ManyToManyfield
            wordtags_with_this_word = Wordtags.objects.filter(wordtag_with_this_word=similarword)
            for wordtag in wordtags_with_this_word:
                similarword.wordtags.remove(wordtag)
            sw.save()
        return HttpResponse(json.dumps({'simwo_id':similarword.id}))
    
def update_show_compoundword(request):
    ''' When the checkbox for 'show_compoundword' is switched '''
    wo_id = request.GET['wo_id']
    show_compoundword = request.GET['show_compoundword']
    show_compoundword = True if show_compoundword in ('True','true') else False # because Jquery sends a string of 'True'/'False'

    this_wordinside = Words.objects.get(id=wo_id)
    compoundword = this_wordinside.compoundword
    compoundword_id_list = []
    # update the database: the words inside the compound word need to be switched for their field 'show_compoundword'
    all_wordinside = Words.objects.filter(compoundword=compoundword) 
    for wordinside in all_wordinside:
        wordinside.show_compoundword = show_compoundword
        wordinside.save()
        compoundword_id_list.append(wordinside.id)

    return HttpResponse(json.dumps({'compoundword_id_list':compoundword_id_list}))
