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
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils.translation import ngettext 
# second party:
import json
import datetime
# third party
# import requests #use to scrap
from urllib.request import Request, urlopen # use to scrarp the dictionary
import html # use to scrarp the dictionary
from bs4 import BeautifulSoup #use to scrap
# local
from lwt.models import *
# helper functions:
from lwt.views._nolang_redirect_decorator import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from lwt.views.termform import *

''' display the text to be read, with lots of javascript...'''
@login_required
@nolang_redirect
def text_read(request, text_id):
    text = Texts.objects.get(id=text_id)
    
    # case where we're opening an archived text. We need to splitText before:
    if text.archived:
        splitText(text)

    # Saving the timestamp for text opening: used in text list
    Texts.objects.filter(id=text_id).update(archived=False, lastopentime= timezone.now())

    word_inthistext = Words.objects.filter(text=text).order_by('sentence_id', 'order')
    
    # increasing the Learning status: Each time the file is open/window refreshed, we calculate whether it
    # was modified more than **24 hours ago**. If yes, update +1 for all word/grouperofsameword/similarword
    # with the basal status of '1' to +1. Max level is '100'.
    if text.lastopentime: # don't run it if the text has never been opened before
        time_from_lastopen = timezone.now() - text.lastopentime
        if time_from_lastopen > datetime.timedelta(hours=24):
            learning_inthistext_groupers = Grouper_of_same_words.objects.filter(
               Q(grouper_of_same_words_for_this_word__text=text )&
               Q(grouper_of_same_words_for_this_word__status__gte=1)).all()
            learning_inthistext_words = Words.objects.filter(grouper_of_same_words__in=learning_inthistext_groupers)
            for wo in learning_inthistext_words:
                wo.status = wo.status + 1 if wo.status + 1 < 100 else 100 # 100 is the status max
            Words.objects.bulk_update(learning_inthistext_words, ['status'])
    
    # calculate the statistic (it's the same stats than in text_list)s
    texttotalword = Words.objects.filter(text=text,isnotword=False).exclude(isCompoundword=True).count()
    textsavedword = Words.objects.filter(text=text,isnotword=False,status__gt=0).exclude(isCompoundword=True).count()
    todo_wordcount = texttotalword - textsavedword 
    todo_wordcount_pc = int(round( todo_wordcount*100 / texttotalword ))
    
    # to have the tooltip displayed. Creating the block of text which the Javascript will read:
    statuses = json.dumps(get_statuses()) # function in _utilities_views
    wordtags = json.dumps(list(Wordtags.objects.values_list('wotagtext',flat=True).order_by('wotagtext')))
    texttags = json.dumps(list(Texttags.objects.values_list('txtagtext',flat=True).order_by('txtagtext')))

    # link to next/previous texts if exists:
    nexttext = Texts.objects.filter(owner=request.user, modified_date__gt=text.modified_date).\
                            order_by('modified_date').first()
    previoustext = Texts.objects.filter(owner=request.user, modified_date__lt=text.modified_date).\
                            order_by('-modified_date').first()

    return render(request, 'lwt/text_read.html',{ 
                'text':text,
                'previoustext':previoustext,'nexttext':nexttext,
                'todo_wordcount': todo_wordcount, 'todo_wordcount_pc':todo_wordcount_pc,
                                                'texttotalword':texttotalword,
                # inside thetext div:
                'word_inthistext':word_inthistext,
                # for tooltip
                'statuses':statuses,'wordtags':wordtags,'texttags':texttags,
        })

def _google_API(content):
    raw_data = content.read()
    data = raw_data.decode("utf-8")
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = None
    else:
        result = html.unescape(re_result[0])
    return [result]
    

def _pons_API(content):
    trans_item_nb = 0
    result = []
    soup = BeautifulSoup(content, 'html.parser')
    div_result = soup.find('div', {'class':'results'})
    if div_result:
        div_entrys = div_result.findChildren('div', {'class': 'entry'}, recursive=False)
        for div_entry in div_entrys:
            h2 = div_entry.find('h2')
            h2.find('sup').extract()
            h2 = h2.get_text().strip()
            result.append({'td1': h2, 'td2': None, 'level': 'h2' })
            div_translations = div_entry.find('div', {'class': 'translations'})
            
            if div_translations:
                for div_translation in div_translations:
                    h3 = div_entry.find('h3').get_text().strip()
                    result.append({'td': h3, 'td': None, 'level': 'h3' })
                    dl_horizontals = div_translation.findChildren('dl', {'class':'dl-horizontal'},
                                                                                          recursive=False)
                    for dl_horizontal in dl_horizontals:
                        origin = dl_horizontal.find('div', {'class':'source'}).get_text().strip()
                        target = dl_horizontal.find('div', {'class':'target'}).get_text().strip()
                        trans_item_nb += 1
                        result.append({'td1': origin, 'td1': target, 'level': None, 'nb': trans_item_nb })
            else:
                dl_horizontals = div_entry.findChildren('dl', {'class':'dl-horizontal'},
                                                                                      recursive=False)
                for dl_horizontal in dl_horizontals:
                    origin = dl_horizontal.find('div', {'class':'source'}).get_text().strip()
                    target = dl_horizontal.find('div', {'class':'target'}).get_text().strip()
                    trans_item_nb += 1
                    result.append({'td1': origin, 'td2': target, 'level': None, 'nb': trans_item_nb })
            

    return (trans_item_nb, result)

''' Helper func for dictwebpage
    allows to clean the webpage to get only the useful content:
    for ex: remove banner, <script> etc... '''
def _clean_body(body, url):
    if 'pons' in url: # Case of a PONS.com website
        body = body.select_one('#container-content')
#         for header in body.select('#page-header'):
#             header.extract()
        body.select_one('.searchbar-tabs').extract()
#         for header in body.select('#feature-nav'):
#             header.extract()
#         for header in body.select('#mobile-page-header'): #useless because the css leaves space for it anyway
#             header.extract()
    return body

def _remove_scriptTag(soup):
    for scr in soup.select('script'):
        scr.extract()
#     for link in soup.select('link'):
#         link.extract()
#         if link.find({'type':'text/css'}):
#             link.extract()
    return soup

''' create dictionary webpage in the bottom right on text_read.html.
Adapted from: makeOpenDictStrJS(createTheDictLink($wb1,$word)) '''
def dictwebpage(request):
    # case 1:  (OUTDATED since Glosbe doesn't work anymore) It needs to fetch an API. 
    # AJAX has fetched the JSON on the wwww, then 
    # the JSON obj from the www is sent to the view dictwebpage which processes it and 
    # and sends back html.
    if 'json_obj' in request.GET.keys():
        parsed_json_obj = json.loads(request.GET['json_obj'])
        return render(request, 'lwt/_glosbe_api.html', {'result': parsed_json_obj}) 

    # case 2:  AJAX sends the link to process to the view dictwebpage, 
    # and the view sends backs a JSON containing the string URL. <iframe> displays it then.  
    else:
        word = request.GET['word']
        wbl = request.GET['wbl']

        # case where it's a lookup sentence:
        if 'issentence' in request.GET.keys() and request.GET['issentence'] != '': # no key "issentence" is sent if the value of 'issentence' is empty in AJAX
            wo_id = int(request.GET['issentence'])
            word = Sentences.objects.values_list('sentencetext',flat=True).get(sentence_having_this_word=wo_id)
        finalurl = createTheDictLink(wbl, word) # create the url of the dictionary, integrating the searched word

        # case where we can't put the url in an iframe src. we must request the entire html webpage
        # and will display it in the iframe srcdoc 

        if finalurl[0] == '^' or finalurl[0] == '!': # case where we open into the frame
#             try: # check that the URL is working. else display a well-formed error 
            headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
                    "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}
            reqest = Request(finalurl[1:], headers=headers)
            content = urlopen(reqest)

        if finalurl[0] == '^':
            try:
                soup = BeautifulSoup(content, 'html.parser')
                soup = _remove_scriptTag(soup)
                links = soup.findAll('link')
                link_str = ''
                for link in links:
                    link_str += str(link)
                body = soup.find('body')
                body_str = str(_clean_body(body, finalurl))
                html = link_str + body_str 
            except:
                html = render_to_string('lwt/dictwebpage_not_working.html') 
            result_str = escape(html)
            return HttpResponse(json.dumps(result_str)) 

        if finalurl[0] == '!': # this dictionary uses my custom APIs (for ex. Google translate)
            if 'https://translate.google.com' in finalurl:
                translation_result = _google_API(content)
                context = {'url':finalurl[1:], 'url_name': 'Google Translate', 'trans_item_nb':len(translation_result),
                           'translation_result':translation_result, 'word_OR_sentence_origin':word} 
            if 'pons.com/translate' in finalurl:
                trans_item_nb, translation_result = _pons_API(content)
                context = {'url':finalurl[1:], 'url_name': 'Pons.com', 'trans_item_nb':trans_item_nb,
                           'translation_result':translation_result, 'word_OR_sentence_origin':word} 
            return render(request, 'lwt/_translation_api.html', context) 

        return HttpResponse(json.dumps(finalurl)) # case where we open into a new window

''' NOT USED FINALLY '''
''' called by AJAX by the form in text_read: shows a list of sentences where the term appears '''
def NOTUSEDFUNCTIONshow_sentence(request):
    wo_ids = request.GET['wo_ids']
    wo_ids = json.loads(wo_ids)
    wo_wordtexts = []
    # if compoundword, they must be present in the same sentence, but order is not important here.
    sentences_with_the_same_wordtext = Sentences.objects.all().order_by('sentencetext')
    for idx, wo_id in enumerate(wo_ids):
        word = Words.objects.get(id=wo_id)
        wordtext = word.wordtext
        wo_wordtexts.append(wordtext)
        sentences_with_the_same_wordtext = sentences_with_the_same_wordtext.\
                    filter(language=word.language).\
                    filter(sentence_having_this_word__wordtext=wordtext)
    display_sentences_with_the_same_wordtext = []
    # display the little '**' '**' around the words
    for sentence_with_the_same_wordtext in sentences_with_the_same_wordtext: # loop over the sentences
        # get all the words inside this sentence:
        words_in_this_sentence = Words.objects.filter(sentence=sentence_with_the_same_wordtext).all().order_by('order')
        sentenceList = []
        for wo in words_in_this_sentence: #  loop inside the sentence: replace the 'word' by '**word**' (that's cooler!)
            if wo.wordtext in wo_wordtexts:
                sentenceList.append('**'+wo.wordtext+'**')
            else:
                sentenceList.append(wo.wordtext)
        display_sentences_with_the_same_wordtext.append(''.join(sentenceList))
    sentences_for_json = list(zip(sentences_with_the_same_wordtext.\
                                        values_list('text__id','text__title'),\
                                 display_sentences_with_the_same_wordtext))
    sentences_json = json.dumps(sentences_for_json)
    return JsonResponse(sentences_json, safe=False)

''' search_possiblesimilarword NOT USED FINALLY (it was called by AJAX)'''
def NOTUSEDFUNCTIONsearch_possiblesimilarword(request): 
    ''' called by AJAX by the form in text_read: shows a list of words, similar to the given word ''' 
    wo_id = request.GET['wo_id']
    word = Words.objects.get(id=wo_id)
    searchboxtext = request.GET['searchboxtext']
    # search with the 3 first letters of the given word. research is made more accurate with the search 
    # box by the user.
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

''' called by AJAX by the form in termform: 
- a word is considered as similar: copy the data from the word to the similar one (and use a Grouper.
- undoing this: delete the similar word '''
def create_or_del_similarword(request):
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
    
''' When the checkbox for 'show_compoundword' is switched '''
def update_show_compoundword(request):
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

''' mark all the remaining words in the sentence as known'''
def iknowall(request):
    wo_id = request.GET['wo_id']
    thisword_sentence = Sentences.objects.filter(sentence_having_this_word__id=wo_id).first()
    wo_id_to_update_in_ajax = list(Words.objects.filter(Q(sentence=thisword_sentence)&Q(status=0)).values_list('id', flat=True))
    Words.objects.filter(Q(sentence=thisword_sentence)&Q(status=0)).update(status=100)
    # display the message
    count = len(wo_id_to_update_in_ajax)
    html = render_to_string('lwt/term_message.html', { 'head_message':_('I KNOW ALL'), 
        'content_message': ngettext('%(count)d word has successfully been marked as Well-Known.', 
             '%(count)d words have successfully been marked as well-known.', count)%{'count': count,}
                            })
    # Get the first word of next sentence: used to make it selected after keyboardshortcut Altr+K
    firstWord_of_nextSentence = Words.objects.filter(Q(sentence_id__gt=thisword_sentence.id)&\
                                                     Q(status=0)&\
                                                     Q(text_id=thisword_sentence.text.id)).\
                                                    exclude(isnotword=True).first()
    
    if (not firstWord_of_nextSentence):
        firstWord_of_nextSentence_id = False
    else:
        firstWord_of_nextSentence_id = firstWord_of_nextSentence.id
        
    return HttpResponse(json.dumps({'html':html, 'wo_id_to_update_in_ajax':wo_id_to_update_in_ajax,
                                            'wowordtext':'', 'wostatus':100,
                                            'iscompoundword': False,
                                            'woromanization':'',
                                            'wotranslation':'',
                                            'cowostatus':'',
                                            'cowotranslation':'',
                                            'coworomanization':'',
                                            'firstWord_of_nextSentence': firstWord_of_nextSentence_id
                                            }))
