""" Helper functions. Guided by the 'utilities.inc.php' file in lwt
    a collection of helper functions. """
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, F, CharField, Value
from django.db.models.expressions import Case, When
from django.utils.translation import ugettext as _
from django.core.serializers import serialize
from django.utils import timezone
# second party
import os
import re
import json 
import urllib
from datetime import timedelta
# local
from lwt.views._setting_cookie_db import *
from lwt.constants import MAX_WORDS
if __name__ != '__main__':
    from lwt.models import *

''' get the current database size and put it in cookie (if not found in cookie)'''
def get_word_database_size(request):
    database_size = getter_settings_cookie('database_size', request)
    if not database_size:
        database_size = Words.objects.filter(owner=request.user).count()
        setter_settings_cookie('database_size', database_size, request)
    return database_size

''' the Words model has changed, update the count of database_size'''
def set_word_database_size(request):
    database_size = Words.objects.filter(owner=request.user).count()
    setter_settings_cookie('database_size', database_size, request)

''' helper function for load_table: the built-in ajax in bootstrap-table
sends a GET request: we get the parameters sent '''
def requesting_get_by_table(request, model):
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    sort_modif = '-'+sort if order == 'desc' else sort
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    offset_modif = int(offset)
    limit_modif = int(limit)

    if model == Words:
        all_words =  model.objects.exclude(Q(isnotword=True)&Q(isCompoundword=False)).\
            filter(owner=request.user).distinct() # don´t know why but theere are in double... so: distinct()
        # sorting on Extra_field: we can't use directly the 'sort_modif' which is on ly 'extra_field'
        if sort not in [f.name for f in model._meta.get_fields()]:
            pattern = r'(?<="'+sort+'":\s").+(?=")'
            model_result = all_words.annotate(**{sort: Case(
                                                        When(extra_field__iregex=pattern, then='extra_field'),
                                                        output_field=CharField(),
                                                        default=Value("Not matched"))
                                                 })
            model_result = model_result.order_by(sort)
#             .order_by(extrafield_val)
        else:
            model_result = all_words.order_by(sort_modif).order_by(sort_modif).all()
    if model == Texts:
        model_result = model.objects.filter(owner=request.user).all().order_by(sort_modif)
    return order, sort, sort_modif, offset, offset_modif, limit, limit_modif, model_result

''' convert a queryset into a bootstrap-table data format '''
def serialize_bootstraptable(queryset, total):
    json_data = serialize('json', queryset)
    json_final = {"total": total, "rows": []}
    data = json.loads(json_data)
    for item in data:
        del item["model"]
        item["fields"].update({"id": item["pk"]})
        item = item["fields"]
        json_final['rows'].append(item)
    return json_final

''' helper function for list_filtering'''
def create_filter(filter_type, filter_list_json):
    if filter_list_json:
        filter = json.loads(filter_list_json)
        for idx, filter_id in enumerate(filter):
            # special case for latopentime filter
            if filter_type == 'lastopentime':
                filter_args = time_filter_args(filter_id)
            else:
                filter_id = int(filter_id)
                filter_args = {filter_type: filter_id}
            
            if idx == 0:
                filter_Q = Q(**filter_args)
            else:
                filter_Q |= Q(**filter_args)
        try:
            return filter_Q
        except NameError: # if the dict is empty. for ex: filter_type : []
            filter_args = {filter_type: None}
            return Q(**filter_args)
    else:# no cookie defined 
        return Q() # don´t filter on this
        #filter_args = {filter_type: -1}
        return Q(**filter_args) 

'''special func because time filter is special...
possible_time = [
    {'week': '[0,4]', 'string':_('< 1 week ago')},
    {'week': '[4,12]', 'string': _('1 wk - 3 mo ago')},
    {'week': '[12,24]', 'string': _('3 mo - 6 mo ago')},
    {'week': '[24,-1]', 'string':_('> 6 months ago')} 
    ]'''
def time_filter_args(week_json):
    now = timezone.now()
    week = json.loads(week_json)
    if week[1] == -1: # it's older than 6 months
        length_of_time = timedelta(weeks=week[0])
        cutout_date = now - length_of_time
        filter_args = {'lastopentime__lte':cutout_date}
    else:
        # for the recent cutout date:
        recent_length_of_time = timedelta(weeks=week[0])
        recent_cutout_date = now - recent_length_of_time
        # for the ancient cutout date:
        ancient_length_of_time = timedelta(weeks=week[1])
        ancient_cutout_date = now - ancient_length_of_time

        filter_args = {'lastopentime__gt': ancient_cutout_date, 'lastopentime__lte': recent_cutout_date}
    return filter_args

''' filter the texts/terms displayed inside bootstrap-table. we use the cookies if they are set 
    called by: lwt/views/load_texttable 
    @model  the model will be filtered. for ex: ´Texts´ for load_texttable
    @request 
'''
def list_filtering( model, request):
    # the User is setting the filters
    if request.method == 'POST': 
        lang_filter_json = request.POST['lang_filter']
        if isinstance(model.first(), Texts): # texts table is filtered
            tag_filter_json = request.POST['tag_filter']
            time_filter_json = request.POST['time_filter']
        if isinstance(model.first(), Words): # words table is filtered 
            text_filter_json = request.POST['text_filter']
            status_filter_json = request.POST['status_filter']
            wordtag_filter_json = request.POST['wordtag_filter']
    # only getting the filter
    else: 
        lang_filter_json = getter_settings_cookie('lang_filter', request)
        if isinstance(model.first(), Texts):
            tag_filter_json = getter_settings_cookie('tag_filter', request)
            time_filter_json = getter_settings_cookie('time_filter', request)
        if isinstance(model.first(), Words):
            text_filter_json = getter_settings_cookie('text_filter', request)
            status_filter_json = getter_settings_cookie('status_filter', request)
            wordtag_filter_json = getter_settings_cookie('wordtag_filter', request)
    # put this inside cookies (the func setter_settings_cookie is in lwt/views/_setting_cookie_db.py):
    setter_settings_cookie('lang_filter', lang_filter_json, request)
    if isinstance(model.first(), Texts): # texts table is filtered
        if tag_filter_json: setter_settings_cookie('tag_filter', tag_filter_json, request)
        if time_filter_json: setter_settings_cookie('time_filter', time_filter_json, request)
    if isinstance(model.first(), Words): # words table is filtered
        setter_settings_cookie('text_filter', text_filter_json, request)
        setter_settings_cookie('status_filter', status_filter_json,
                                                            request)
        setter_settings_cookie('wordtag_filter', wordtag_filter_json, request)
    # Create the filters for lang
    filter_Q_lang = create_filter('language_id', lang_filter_json)
    if isinstance(model.first(), Texts): # texts table is filtered
        filter_Q_tag = create_filter('texttags__id', tag_filter_json)
        filter_Q_time = create_filter('lastopentime', time_filter_json)
    if isinstance(model.first(), Words): # words table is filtered
        filter_Q_text = create_filter('text_id', text_filter_json) 
        filter_Q_status = create_filter('status', status_filter_json)
        filter_Q_wordtag = create_filter('wordtags', wordtag_filter_json)
    # And finally filter the models:
    if isinstance(model.first(), Texts): # texts table is filtered
        results = model.filter(filter_Q_lang).\
                        filter(filter_Q_time).\
                        filter(filter_Q_tag).\
                        distinct() # because many2many, a text can have 2 tags. don't count 2 times so...
#                         filter(filter_Q_tag).\
    if isinstance(model.first(), Words): # words table is filtered
        results = model.filter(filter_Q_lang).\
                        filter(filter_Q_status).\
                        filter(filter_Q_wordtag).\
                        filter(filter_Q_text)
    
    return results

def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError 

''' clean after uploading the file: remove the file in the dir and the Object'''
def delete_uploadedfiles(Model_to_delete):
    for dirpath, subdirs, files in os.walk(settings.MEDIA_ROOT):
        for file in files:
            os.remove(os.path.join(dirpath, file))
    qrs = Model_to_delete.objects.all()
    for qr in qrs:
        qr.delete()

""" Does the language with this ID 'currentlang' exists in db? """
''' NOT USED
def validateLang(currentlang):
    if currentlang != '':
        if not Languages.objects.filter(owner=text.owner).get(id=int(currentlang)):
            currentlang = ''
    return currentlang '''

""" Is the tag is used in the texts? Return '' if not """
'''NOT USED
def validateTextTag(currenttag, currentlang):
    if currenttag != '' and currenttag != -1:
        if currentlang != '' and currentlang != -1:
            t = Texts.objects.filter(owner=text.owner).filter(language__id=currentlang).values_list(
                'texttags', flat=True).distinct()
        else:
            # get the list of the distict tags used in the texts
            t = Texts.objects.filter(owner=text.owner).values_list('texttags', flat=True).distinct()
        r = Texttags.objects.filter(owner=text.owner).filter(id__in=t).count()
        currenttag = '' if r == 0 else currenttag
    return currenttag'''
    
''' Helper function for splitText. split the text into sentence '''
def splitSentence(t, splitSentenceMark):
    # split by paragraph (end of line)
    split_pat = r'(\n+)'
    paragraphs = re.split(split_pat, t)
    # split by dedicated character for end of sentence:
    temp_t = []
    index = 0
    # find sentences inside each paragraph. the Delimiter is appended to the sentence found just before 
    for paragraph in paragraphs:
        split_pat  = r'([' + re.escape(splitSentenceMark) + '])'
        temp_split = re.split(split_pat, paragraph)
        # appending the delimiter to the sentence (the element before in the temp_t list)
        for idx, s in enumerate(temp_split):
            if s == '': # split always create some weird blank element around the delimiter: discard them
                pass
            else: # appending the delimiter to the element before: which is the sentence found
                if idx %2 == 0:
                    temp_t.append(s)
                    index += 1
                elif idx %2 != 0:
                    temp_t[index-1] += s
    return temp_t 
    
''' split the text into sentences.
    and then insert sentences/words in DB '''
def splitText(request, text):
    removeSpaces = text.language.removespaces # Used for Chinese,Jap where the white spaces are not used.
    splitEachChar = text.language.spliteachchar
    splitSentenceMark = text.language.regexpsplitsentences
    noSentenceEnd = text.language.exceptionssplitsentences #"Mr.|Dr.|[A-Z].|Vd.|Vds." 
    termchar = text.language.regexpwordcharacters
    replace = text.language.charactersubstitutions.split("|") # some weird apostrophes are listed, triple dots etc.
    rtlScript = text.language.righttoleft
    ######## PRE-PROCESSING ##############################################################################
    t = text.text
    
    # reverse the text if righttoleft language (like Hebrew/arab)
#     if rtlScript:
#         word_split_pattern = r'([^'+termchar+']+)' # pattern used to separate Hebrew words with the rest
#         t_splitted = re.split(word_split_pattern, t)
#         t_splitted = [i for i in t_splitted if i] # remove empty element created by the split
#         t = ''.join(t_splitted[::-1]) # reverse the list than join it again to recreate the text, inversed

    t = t.replace('’', '\'') # strange pb with the ', which is different from ’

#         fromto = value.strip().split("=")
#         if len(fromto) >= 2:
#             t = t.replace(fromto[0].strip(), fromto[1].strip())
#         t = t.strip()

    if noSentenceEnd != '': # 'M.John' must not be cut into 2 sentences. replace the dot with an 'hyphenation point'
        noSentenceEnd = noSentenceEnd.replace('.', '\.') #because regex takes the '.' for a special char...
        t = re.sub(r'(' + noSentenceEnd+ ')', lambda a: (a.group(1)[:-1])+r'‧', t)

    sentences = splitSentence(t, splitSentenceMark)

    ################################################
    # Split: insert sentences/textitems entries in DB
    for sentID,sentTxt in enumerate(sentences): # Loop on each sentence
        new_words_created = []
        with transaction.atomic(): # allow bulk transaction
            newsentence = Sentences.objects.create(owner=text.owner,language=text.language,
                                                   sentencetext=sentTxt, order=sentID+1,text=text) # create each sentence
            # splitting the words inside the sentence:
            word_split_pattern = r'([^'+termchar+']+)' # non character are used as the end of word

            sentList = re.split(word_split_pattern, sentTxt) # ['This',' ','is',' ','good','.',' ']
            sentList = [i for i in sentList if i] # remove the empty item created by re.split
            # Special case: it's the delimiter: the '.' at the end of the sentence for ex.
            if len(sentList) > 1 and not re.match(r'[^\W\d_]', sentList[-1]):
                lastitem_isnotword = sentList.pop() 
            else:
                lastitem_isnotword = False
                
            # split each character of each 'word' if it's Japanese/Chinese:
            if splitEachChar: # do we make each character a word? (used in Chinese,Jap)
                temp_sentList = []
                for wordidx,word in enumerate(sentList): 
                    if re.search(r'[' + termchar +  ']', word): # match only word
                        # this regex pattern matches only Japanese/Chinese word.
                        splitEachChar_List = re.split(r'(['+termchar+'])', word)
                        splitEachChar_List = [i for i in splitEachChar_List if i] # remove the empty item created by re.split
                        temp_sentList.extend(splitEachChar_List)
                    else: # the element doesn't contain any Jap/Chinese character. not to spit in character
                        temp_sentList.append(word)
                sentList = temp_sentList

            for wordidx,word in enumerate(sentList): 
                if re.search(r'[' + termchar +  ']', word): 
                    # create a Grouper of same words by default with the same id than the word:
                    wo = Words.objects.create(owner=text.owner,language=text.language, 
                                              sentence=newsentence,text=text,order=wordidx, \
                                                wordtext=word, \
#                                               wordtext=remove_spaces(word,removeSpaces), \
                                              isnotword=False)
                    grouper_of_same_words = Grouper_of_same_words.objects.create(owner=text.owner,id=wo.id)
                    wo.grouper_of_same_words = grouper_of_same_words
                    wo.save()
                    new_words_created.append(wo)
                else: # Non-words
                    Words.objects.create(owner=text.owner,language=text.language, sentence=newsentence,text=text,order=wordidx, \
                                     wordtext=word, isnotword=True)

            # Special case: it's the delimiter: the '.' at the end of the sentence for ex.
            if lastitem_isnotword:
                Words.objects.create(owner=text.owner,language=text.language, sentence=newsentence,text=text,order=wordidx, \
                             wordtext=lastitem_isnotword, isnotword=True)
    ################## PARSING THE TEXT FOR SIMILAR WORD: #########################################################################
    # We check whether the word, written similarly, hasn't been defined elsewhere:
    # we sort the list to accelerate the speed inside the loop:
    new_words_created_sorted = sorted(new_words_created, key=lambda word: word.wordtext)
    temp_word = ''
    for word in new_words_created_sorted:
        if temp_word != '':
            if word.wordtext == temp_word.wordtext: # it's the same word than the word before in the list:
                word.grouper_of_same_words = temp_word.grouper_of_same_words
                word.status = temp_word.status
                word.save()
                temp_word = word
        else: # word with a different wordtext: we search for other words in other texts:
            similar_wo = Words.objects.filter(language=text.language).exclude(text=text).filter(wordtext=word.wordtext).first()
            if similar_wo:
                word.grouper_of_same_words = similar_wo.grouper_of_same_words
                word.status = similar_wo.status
                word.save()
                temp_word = word

    ###################### Calculate how many words are for this language: Display a warning if too many words: ####################
    total_words_in_this_lang = Words.objects.filter(owner=request.user, language=text.language).count()
    if total_words_in_this_lang > MAX_WORDS:
        messages.warning(request, _('With this additional text, you\'ve got now ') + \
                        str(total_words_in_this_lang) + _(' words for ') + text.language.name + \
                        _('. This could slow the program a lot. Please consider archiving some texts.'))

# IS IT USEFUL???
# def remove_spaces(s,remove):
#     ''' some cleaning for the splitting in textitems function '''
#     if remove:
#         return re.sub(r'\s{1,}', r'', s)  
#     else:
#         return s

''' some other cleaning for the splitting in textitems function '''
def repl_tab_nl(s):
    s = re.sub(r'[\r\n\t]', r' ', s)
    s = re.sub(r'\r\n', r' ', s)
    s = re.sub(r'\s', r' ', s)
    s = re.sub(r'\s{2,}', r' ', s)
    return s.strip()

''' original php function converted in python ''' 
def isset(variable):
    return variable in locals() or variable in globals()

''' Converts the field in text, annotatedtx to json format
to be readable inside the javascript part in text_read '''
def annotation_to_json(ann):
    if ann == '':
        return "{}"
    arr = {}
    items = re.split(r'[\n]', ann)
    for item in items:
        vals = re.split(r'[\t]', item)
        if len(vals) > 3 and vals[0] >= 0 and vals[2] > 0:
            arr[vals[0]-1] = [vals[1],vals[2],vals[3]]
    return json.dump(arr)

''' don't know what it's doing...'''
def makeStatusClassFilter(status):
    if status == '':
        return ''
    ls = [1,2,3,4,5,98,99]
    if status == 599:
        makeStatusClassFilterHelper(5,ls)
        makeStatusClassFilterHelper(99,ls)
    elif status < 6 or status > 97:
        makeStatusClassFilterHelper(status,ls)
    else:
        start = int(status) / 10
        end = status - start*10
        for i in range(start,end):
            makeStatusClassFilterHelper(i,ls)
    r = ''
    for v in ls:
        if v != -1:
            r += ':not(.status'+v+')'
    return r


''' don't know what it's doing...'''
def makeStatusClassFilterHelper(status,ls):
    try:
        pos = ls.index(status)
        ls[pos] = -1
    except ValueError: # not found
        pass

''' escapes everything to "Â¤xx" but not 0-9, a-z, A-Z, and unicode >= (hex 00A5, dec 165) '''
''' What's the need of this???...'''
def strToClassName(mystring):
    l = len(mystring)
    r = ''
    for i in range(l):
        c = mystring[i:i+1]
        o = ord(c)
        if o < 48 or (o > 57 and o < 65) or (o > 90 and o < 97) or (o > 122 and o < 165):
            r += 'Â¤'+strToHex(c)
        else: 
            r += c
    return r

''' What's the need of this???...'''
def strToHex(mystring):
    myhex=''
    for c in mystring:
        h = hex(ord(c))
        if len(h) == 1: 
            myhex += "0"+h
        else:
            myhex += h
    return myhex.upper()

''' CONSTANTS (I know, it's not me...) used inside text_read when displaying the tooltip '''
    #TODO increase the status of learning words each time we open a text that contains this word??
def get_statuses():
    statuses = { 0 : {"abbr" :   "0", "name" : _("Unknown")},
                1 : {"abbr" :   "1", "name" : _("Learning")},
                100 : {"abbr" : _("WKn"), "name" : _("Well Known")},
                101 : {"abbr" : _("Ign"), "name" : _("Ignored")}, }
    return statuses

''' same as above but with using parameter. NOTE: It allows to get intermediate number
    for example: 56, would be considered as 'Learning'. '''
def get_name_status(nb):
    if nb == 0:
        return _("Unknown")
    if nb == 100:
        return _("Well Known")
    if nb == 101:
        return _("Ignored")
    else:
        return _('Learning')
        
''' 
- called by view dictwebpage to create the dict link in text_read bottomright 
- called by pgm.js:  create_link_webdict(wblink1,wblink2,wblink3,txt,txid,torder)
createTheDictLink(wblink1,txt,'Dict1','Lookup Term: ') + =>http://127.0.0.1/trans.php?x=2&i=http%3A//www.wordreference.com/enfr/%23%23%23&t=This  
createTheDictLink(wblink2,txt,'Dict2','') +
createTheDictLink(wblink3,txt,'GTr','') + ...'''
def createTheDictLink(u,t): 
    # Case 1: url without any ###: append UTF-8-term
    # Case 2: url with 1 ###: substitute UTF-8-term
    # Case 3: url with 2 ###enc###: substitute enc-encoded-term
    url = u.strip()
    trm = t.strip()
    pos = url.upper().find('###')
    if pos > 0: # ### found
        pos2 = url.upper().rfind('###')
        if (pos2-pos-3) > 1:   # 2 ### found
            enc = url[(pos+3):pos2].strip()
            r = url[:pos]
            r += urllib.parse.quote_plus(trm.decode(enc).encode('UTF-8'))
            if (pos2+3) < len(url):
                r += url[(pos2+3):]
        elif pos == pos2: # 1 ### found
            replac = '+' if trm == '' else urllib.parse.quote_plus(trm)
            r = url.replace("###", replac)
    else:  # no ### found
        r = urllib.parse.quote_plus(trm)
    return r

'''
def texttodocount2(text):
    # Update the number of word to do and Display the "I KNOW ALL" button (if it's still useful) 
    c = textwordcount(text) - textworkcount(text)
    if c > 0: 
        return '<span title="To Do" class="status0">&nbsp;' + str(c)+'&nbsp;</span>&nbsp;&nbsp;&nbsp;<input type="button" onclick="iknowall(' +text+');" value=" I KNOW ALL " />'
    else
        return '<span title="To Do" class="status0">&nbsp;' + str(c)+'&nbsp;</span>'
}
'''


if __name__ == '__main__':
    splitSentenceMark = '.!?:;。！？：；'
    txt = 'this is first sentence...\n\n And this is another one. This is the last one. Is it!?! Indeed it is.'

    r = splitSentence(txt, splitSentenceMark)
    print(r)
    print(''.join(r))



