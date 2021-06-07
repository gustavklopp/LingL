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
from django.templatetags.static import static # to use the 'static' tag as in the templates
# second party:
import json
import datetime
import re
# third party
# import requests #use to scrap
from urllib.request import Request, urlopen # use to scrap the dictionary
from urllib import parse # set the encoding for the URL
import html # use to scrap the dictionary
from bs4 import BeautifulSoup #use to scrap
# local
from lwt.models import *
# helper functions:
from lwt.views._nolang_redirect_decorator import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from lwt.views.termform import *
from lwt.constants import STATUS_CHOICES

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
    texttotalword = text.wordcount_distinct
    textsavedword = Words.objects.filter(text=text,isnotword=False,status__gt=0).exclude(isCompoundword=True).count()
#     texttotalword = Words.objects.filter(text=text,isnotword=False).exclude(isCompoundword=True).count()
    todo_wordcount = texttotalword - textsavedword 
    todo_wordcount_pc = int(round( todo_wordcount*100 / texttotalword ))
    
    # to have the tooltip displayed. Creating the block of text which the Javascript will read:
    statuses = json.dumps(STATUS_CHOICES) 
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
    

def _pons_API(content, url):
    from django.utils.translation import get_language_info

    soup = BeautifulSoup(content, 'html.parser')
    # Sometimes Pons displays the targeted language in the second block, sometimes in the second...
    pattern = r'(?<=en\.pons\.com/translate/)\w+(?=-)'
    origin_lang = re.search(pattern, url).group().lower()

    divs_lang = soup.find_all('div', {'class':'lang'})
    div_targets = []
    for div_lang in divs_lang:
        # we must determine what is the origin language for each block
        div_lang_origin = div_lang['id']
        is_origin_lang_first = origin_lang == get_language_info(div_lang_origin)['name'].lower()
        if is_origin_lang_first:
            div_targets.extend(div_lang.find_all('div', {'class': 'target'}))
        else:
            div_targets.extend(div_lang.find_all('div', {'class': 'source'}))
            
    for idx, div_target in enumerate(div_targets):
        trans_item = div_target.get_text().strip()
        new_tag = '<span  title="{0}" class="hover_pointer" onclick="addTranslation(\'{1}\');">'
        new_tag += '<img src="{2}" alt="Copy" />&nbsp;<span id="trans_item_{3}">{1}</span>&nbsp;'
        new_tag += '<span class="text-muted" title="{4}">[{3}]</span> </span>'
        new_tag = new_tag.format(_('Copy this translation'), trans_item, static('lwt/img/icn/tick-button.png'), 
                                idx+1, _('keyboard shortcut'))
        tag_soup = BeautifulSoup(new_tag, 'html.parser').find('span')
        div_target.replace_with(tag_soup)
    html = _clean_soup(soup, url)
    return html

def _dictcc_API(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')
    idx_item = 0
    for row in rows:
        if not row.has_attr('id'):
            continue
        idx_item += 1
        td = row.find_all('td')[1]
        trans_item = td.get_text().strip()
        new_tag = '''
            <td><span  title="Copy" class="hover_pointer" onclick="addTranslation('{0}');">
                <img src="{1}" alt="Copy" />&nbsp;<span id="trans_item_{2}">{0}</span>&nbsp;<span class="text-muted" 
                title="{3}">[{2}]</span>
            </span></td>'''.format(trans_item, static('lwt/img/icn/tick-button.png'), idx_item, _('keyboard shortcut'))
        tag_soup = BeautifulSoup(new_tag, 'html.parser').find('td')
        td.replace_with(tag_soup)
    html = _clean_soup(soup, url)
    return html

def _wordref_API(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    td_towrds = soup.find_all('td',{'class':'ToWrd'})
    idx_item = 0
    for td_towrd in td_towrds:
        if td_towrd.get_text() == 'Englisch':
            continue
        idx_item += 1
        spans = td_towrd.find_all('span')
        for span in spans:
            if span.has_attr('title'):
                continue
            span.extract()
        trans_item = td_towrd.get_text().strip()
        new_tag = '''
            <td class="ToWrd"><span  title="{0}" class="hover_pointer" onclick="addTranslation('{1}');">
                <img src="{2}" alt="Copy" />&nbsp;<span id="trans_item_{3}">{1}</span>&nbsp;<span class="text-muted" 
                title="{4}">[{3}]</span>
            </span></td>'''.format(_('Copy this translation'), trans_item, 
                                   static('lwt/img/icn/tick-button.png'), idx_item, _('keyboard shortcut'))
        tag_soup = BeautifulSoup(new_tag, 'html.parser').find('td')
        td_towrd.replace_with(tag_soup)
    span_romans = soup.find_all('span',{'class':'roman'})
    for span_roman in span_romans:
        idx_item += 1
        spans = span_roman.find_all('span')
        for span in spans:
            if span.has_attr('title'):
                continue
            span.extract()
        trans_item = span_roman.get_text().strip()
        new_tag = '''
            <span  title="{0}" class="roman hover_pointer" onclick="addTranslation('{1}');">
                <img src="{2}" alt="Copy" />&nbsp;<span id="trans_item_{3}">{1}</span>&nbsp;<span class="text-muted" 
                title="{4}">[{3}]</span>
            </span>'''.format(_('Copy this translation'), trans_item, 
                              static('lwt/img/icn/tick-button.png'), idx_item, _('keyboard shortcut'))
        tag_soup = BeautifulSoup(new_tag, 'html.parser').find('span')
        span_roman.replace_with(tag_soup)
    html = _clean_soup(soup, url)
    return html

def _wiki_API(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    ols = soup.find_all('ol')
    idx_item = 0
    for ol in ols:
        for li in ol.find_all('li'):
            idx_item += 1
            to_be_added_str = ''
            span_hqtoggle = li.find('span', {'class':'HQToggle'})
            if span_hqtoggle:
                to_be_added_str += str(span_hqtoggle)
                span_hqtoggle.extract()
            dl = li.find('dl')
            if dl:
                to_be_added_str += str(dl)
                dl.extract()
            trans_item = li.get_text().strip()
            new_tag = '''
                <li><span  title="{0}" class="roman hover_pointer" onclick="addTranslation('{1}');">
                    <img src="{2}" alt="Copy" />&nbsp;<span id="trans_item_{3}">{1}</span>&nbsp;<span class="text-muted" 
                    title="{4}">[{3}]</span>
                </span>{5}</li>'''.format(_('Copy this translation'), trans_item, 
                                            static('lwt/img/icn/tick-button.png'), idx_item,
                                           _('keyboard shortcut'), to_be_added_str)
            tag_soup = BeautifulSoup(new_tag, 'html.parser').find('li')
            li.replace_with(tag_soup)
    html = _clean_soup(soup, url)
    return html

def _wiki_API_redirect(error, finalurl, word_escaped):
    soup = BeautifulSoup(error, 'html.parser')
    didyoumean = soup.find('span', {'id':'did-you-mean'})
    if didyoumean:
        didyoumean_a = didyoumean.find('a') # --> '/wiki/thisotherspelledword'
        didyoumean_word = didyoumean_a['href'].split('/')[-1]
        didyoumean_word_escaped = parse.quote(didyoumean_word)
        finalurl = finalurl.replace(word_escaped, didyoumean_word_escaped)
    return finalurl

''' Helper func for dictwebpage (and _pons_API()
    allows to clean the webpage to get only the useful content:
    for ex: remove banner, <script> etc... '''
def _clean_soup(soup, url):
    # Remove all <script></script>
    for scr in soup.select('script'):
        scr.extract()
    # We'll keep only <link> and <body>
    links = soup.findAll('link')
    link_str = ''
    for link in links:
        # further editing of <link> or some API (css file messsing up with my own style)
        str_link = str(link)
        # bootstrap style loaded by pons.com are messing up with my own style
        if 'pons' in url  and 'bootstrap_dict_catalogue' in str_link:
            continue
        if 'dict.cc' in url and 'dict.cc/inc/dict.css' in str_link:
            continue
        # for Wordreference.com, the style is inline in fact, in a <style> tag
        if 'wiktionary' in url and 'rel="stylesheet"' in str_link:
            continue
        link_str += str_link
    body = soup.find('body')
    # further editing of the <body> for some API
    if 'pons' in url: # Case of a PONS.com website, some div can be removed
        body_pageheader = body.select_one('#page-header')
        if body_pageheader:
            body_pageheader.extract()
        body_containercontent = body.select_one('#container-content')
        if body_containercontent:
            body.select_one('.searchbar-tabs').extract()
        if result_section_nav := body.select_one('#result-section__nav'):
            result_section_nav.extract()
        if result_section_header := body.find_all('h3', {'class':'result-section__header'}):
            [r.extract() for r in result_section_header]
    if 'wordref' in url:
        body.find('header', {'class':'full-header'}).extract()
        body.find('div', {'id':'ad1'}).extract()
        body.find('div', {'id':'search'}).extract()
    if 'wiktionary' in url:
        div_mwbody = body.find('div', {'class':'mw-body'})
        body = div_mwbody
    body_str = str(body)
    html = link_str + body_str 
    return html

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
        word_escaped = parse.quote(word)
        wbl = request.GET['wbl']

        # case where it's a lookup sentence:
        if 'issentence' in request.GET.keys() and request.GET['issentence'] != '': # no key "issentence" is sent if the value of 'issentence' is empty in AJAX
            wo_id = int(request.GET['issentence'])
            word = Sentences.objects.values_list('sentencetext',flat=True).get(sentence_having_this_word=wo_id)
            word_escaped = parse.quote(word)
        finalurl = wbl.replace('<WORD>', word_escaped)
#         finalurl = createTheDictLink(wbl, word) # create the url of the dictionary, integrating the searched word

        # case where we can't put the url in an iframe src. we must request the entire html webpage
        # and will display it in the iframe srcdoc 

        if finalurl[0] == '^' or finalurl[0] == '!': # case where we open into the frame
#             try: # check that the URL is working. else display a well-formed error 
            headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
                    "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}
            reqest = Request(finalurl[1:], headers=headers)
            try:
                content = urlopen(reqest)
            # catch the redirect from Wiktionary
            except urllib.error.HTTPError as httpError:
                error = httpError.read().decode()
                # wiktionary has a way to redirect to similar word if nothing found
                if 'wiktionary' in finalurl:
                    redirect_url = _wiki_API_redirect(error, finalurl[1:], word_escaped)
                    reqest = Request(redirect_url, headers=headers)
                    try:
                        content = urlopen(reqest)
                    except:
                        content = error # redirect doesn't work neither, so display the error
                else:
                    content = error 

        if finalurl[0] == '^':
            try:
                soup = BeautifulSoup(content, 'html.parser')
                html = _clean_soup(soup, finalurl)
            except:
                html = render_to_string('lwt/dictwebpage_not_working.html') 
            result_str = escape(html)
            return HttpResponse(json.dumps(result_str)) 

        if finalurl[0] == '!': # this dictionary uses my custom APIs (for ex. Google translate)
            if 'https://translate.google.com' in finalurl:
                translation_result = _google_API(content)
                context = {'url':finalurl[1:], 'url_name': 'Google Translate', 'trans_item_nb':len(translation_result),
                           'translation_result':translation_result, 'word_OR_sentence_origin':word} 
                return render(request, 'lwt/_google_api.html', context) 
            if 'pons.com/translate' in finalurl:
                translation_result = _pons_API(content, finalurl)
                context = {'translation_result':translation_result, 'API_name':'pons'} 
            if 'dict.cc' in finalurl:
                translation_result = _dictcc_API(content, finalurl)
                context = {'translation_result':translation_result, 'API_name':'dictcc'} 
            if 'wordref' in finalurl:
                translation_result = _wordref_API(content, finalurl)
                context = {'translation_result':translation_result, 'API_name':'wordref'} 
            if 'wiktionary' in finalurl:
                translation_result = _wiki_API(content, finalurl)
                context = {'translation_result':translation_result, 'API_name':'wiki'} 
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
