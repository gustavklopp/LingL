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
from datetime import timedelta, datetime
import requests
# local
from lwt.views._setting_cookie_db import *
from lwt.constants import MAX_WORDS_DANGER, MAX_WORDS_NOTICE, MAX_WORDS_WARNING
if __name__ != '__main__':
    from lwt.models import *


''' Get the current date of the release and fetches the date of the latest release on the Github.
    It checks it once in 24 hours (else it checks only cookie)'''
def get_appversion(request):

    # only check once in 24 hours the current version and if there's a new version on the Github release page:
    date_check = getter_settings_cookie('date_check', request)
    now = datetime.now().timestamp()
    if not date_check or date_check - now > 86400: # 24*3600
        # Time to check...

        # the app version is taken from the file appversion.txt which contains the date of the release
        # (this release date txt file is updated when building the Linux version)
        appversiontxt_path = os.path.join(settings.BASE_DIR, 'lwt', 'appversion.txt')
        with open(appversiontxt_path, 'r', encoding="utf8") as appversion_f:
            current_date = appversion_f.read().strip()

        # get the date of the latest release on GIthub:
        resp = requests.get('https://api.github.com/repos/gustavklopp/lingl/releases')
        if resp.status_code == 200:
            releases = resp.json()[:3]
            for release in releases:
                if release['name'].startswith('windows'):
                    release_date_str = release['name'][-10:] # the date is in the end of the string 'linux LingLibre 2016.06.20'
                    release_date_obj = datetime.strptime(release_date_str, '%Y.%m.%d' ) # '2021.06.20'
                    current_date_obj = datetime.strptime(current_date, '%Y.%m.%d')
                    is_outdated = current_date_obj < release_date_obj
                    break

            # and update the cookies
            setter_settings_cookie('date_check', now, request)
            setter_settings_cookie('current_date', current_date, request)
        else: # error accessing Github release page
            return {'current_date':_('<Error accessing Github Server>'), 'is_outdated':True}
    else:
        current_date = getter_settings_cookie('current_date', request)
        is_outdated = False # we assume it's not outdated even if we don't check...
        
    return {'current_date':current_date, 'is_outdated':is_outdated}
   
'''convert the placeholder for the link to the online dictionaries
   for ex.: https://en.pons.com/translate/english-<NAMELC>/### 
           =>      https://en.pons.com/translate/english-chinese/###'''
def convert_placeholder_webdictlink(webdictlink, lang_obj):
        # then change the placeholder string for the translation:
    if '<NAMELC>' in webdictlink: 
        modif_webdictlink = re.sub(r'<NAMELC>', lang_obj['name'].lower(), webdictlink)
    elif '<NAME>' in webdictlink: 
        modif_webdictlink = re.sub(r'<NAME>', lang_obj['name'], webdictlink)
    elif '<2TCODE>' in webdictlink: 
        modif_webdictlink = re.sub(r'<2TCODE>', lang_obj['2T'], webdictlink)
    elif '<1CODE>' in webdictlink or '<GT>' in webdictlink: 
        modif_webdictlink = re.sub(r'<1CODE>', lang_obj['1'], webdictlink)
    return modif_webdictlink

''' Alternative to PostGreSQL 'distinct_on()', which doesn't exist in SQLITE3'''
def distinct_on(mylist, criteria, case_unsensitive=True):
    onlyunique_list = []
    prev_criteria = None
    if case_unsensitive:
        prev_criteria = ''
    for item in mylist:
        if case_unsensitive:
            if getattr(item, criteria).lower() != prev_criteria.lower():
                onlyunique_list.append(item)
        else:
            if getattr(item, criteria) != prev_criteria:
                onlyunique_list.append(item)
        prev_criteria = getattr(item, criteria)
    return onlyunique_list
    
''' get the current database size and put it in cookie (if not found in cookie)'''
def get_word_database_size(request):
    database_size = getter_settings_cookie('database_size', request)
    if not database_size:
        database_size = Words.objects.filter(owner=request.user).count()
        setter_settings_cookie('database_size', database_size, request)
    database_health = 'HEALTHY' # display a message in the footer of each page
    if database_size > MAX_WORDS_NOTICE:
        database_health = 'NOTICE'
    if database_size > MAX_WORDS_WARNING:
        database_health = 'WARNING'
    if database_size > MAX_WORDS_DANGER:
        database_health = 'DANGER'
    return {'database_size':database_size, 'database_health':database_health}

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

'''helper func for create_filter: special func because time filter is special...
possible_time = [
    {'week': '[0,4]', 'string':_('< 1 week ago')},
    {'week': '[4,12]', 'string': _('1 wk - 3 mo ago')},
    {'week': '[12,24]', 'string': _('3 mo - 6 mo ago')},
    {'week': '[24,-1]', 'string':_('> 6 months ago')} 
    {'week': 'null', 'string':_('never opened')} 
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


''' helper function for list_filtering'''
def create_filter(filter_type, filter_list_json):
    if filter_list_json:
        filter_list = json.loads(filter_list_json)
        # special case for filtering on time: if list if empty,
        # we shouldn't display any objects
        if filter_type == 'lastopentime' and not filter_list:
            filter_args = {'lastopentime': timezone.now() + timedelta(days=1)} #1 day in the future
            return Q(**filter_args)
        # special case for filtering on tags and texts: if list if empty, we'll display everything
#         if (filter_type == 'texttags__id' or filter_type == 'wordtags__id'\
#             or filter_type == 'text_id') and not filter_list:
        # Finally, it's better to not filtering when nothing is selected:
        if not filter_list:
            return Q()
        # we shoul display all objects
        for idx, filter_val in enumerate(filter_list):
            # special case for latopentime filter
            if filter_type == 'lastopentime':
                filter_args = time_filter_args(filter_val)
            else:
                if filter_type == 'archived' or filter_type == 'isCompoundword':
                    filter_val = str_to_bool(filter_val)
                else:
                    filter_val = int(filter_val)
                # special case for status "Learning" since we need to take into account 
                # choice 'Learning [0 to 99]' 
                if filter_type == 'status' and filter_val == 1:
                    filter_args = {'status__gt': 0, 'status__lt': 100}
                else:
                    filter_args = {filter_type: filter_val}
            
            if idx == 0:
                filter_Q = Q(**filter_args)
            else:
                filter_Q |= Q(**filter_args)
        # special case to get also the obj never opened
        if filter_type == 'lastopentime' and '[24, -1]' in filter_list:
            filter_args = {'lastopentime':None}
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
            archived_filter_json = request.POST['archived_filter']
        if isinstance(model.first(), Words): # words table is filtered 
            text_filter_json = request.POST['text_filter']
            status_filter_json = request.POST['status_filter']
            wordtag_filter_json = request.POST['wordtag_filter']
            compoundword_filter_json = request.POST['compoundword_filter']
    # only getting the filter
    else: 
        lang_filter_json = getter_settings_cookie('lang_filter', request)
        if isinstance(model.first(), Texts):
            tag_filter_json = getter_settings_cookie('tag_filter', request)
            time_filter_json = getter_settings_cookie('time_filter', request)
            archived_filter_json = getter_settings_cookie('archived_filter', request)
        if isinstance(model.first(), Words):
            text_filter_json = getter_settings_cookie('text_filter', request)
            status_filter_json = getter_settings_cookie('status_filter', request)
            wordtag_filter_json = getter_settings_cookie('wordtag_filter', request)
            compoundword_filter_json = getter_settings_cookie('compoundword_filter', request)
    # put this inside cookies (the func setter_settings_cookie is in lwt/views/_setting_cookie_db.py):
    setter_settings_cookie('lang_filter', lang_filter_json, request)
    if isinstance(model.first(), Texts): # texts table is filtered
        if tag_filter_json: setter_settings_cookie('tag_filter', tag_filter_json, request)
        if time_filter_json: setter_settings_cookie('time_filter', time_filter_json, request)
        if archived_filter_json: setter_settings_cookie('archived_filter', archived_filter_json, request)
    if isinstance(model.first(), Words): # words table is filtered
        setter_settings_cookie('text_filter', text_filter_json, request)
        setter_settings_cookie('status_filter', status_filter_json, request)
        setter_settings_cookie('wordtag_filter', wordtag_filter_json, request)
        setter_settings_cookie('compoundword_filter', compoundword_filter_json, request)
    # Create the filters for lang
    filter_Q_lang = create_filter('language_id', lang_filter_json)
    if isinstance(model.first(), Texts): # texts table is filtered
        filter_Q_tag = create_filter('texttags__id', tag_filter_json)
        filter_Q_time = create_filter('lastopentime', time_filter_json)
        filter_Q_archived = create_filter('archived', archived_filter_json)
    if isinstance(model.first(), Words): # words table is filtered
        filter_Q_text = create_filter('text_id', text_filter_json) 
        filter_Q_status = create_filter('status', status_filter_json)
        filter_Q_wordtag = create_filter('wordtags', wordtag_filter_json)
        filter_Q_compoundword = create_filter('isCompoundword', compoundword_filter_json)
        # special case for filtering on compoundword or not:
        # special case for filtering on compoundword or not:
#         filter_Q_compoundword = Q()
#         if compoundword_filter_json:
#             compoundword_filter = json.loads(compoundword_filter_json)
#             for idx, filter in enumerate(compoundword_filter):
#                 if idx == 0:
#                     if filter == 'cw_display_word':
#                         filter_Q_compoundword = Q(isCompoundword=False)
#                     elif filter == 'cw_display_coword':
#                         filter_Q_compoundword = Q(isCompoundword=True)
#                 else:
#                     if filter == 'cw_display_word':
#                         filter_Q_compoundword |= Q(isCompoundword=False)
#                     elif filter == 'cw_display_coword':
#                         filter_Q_compoundword |= Q(isCompoundword=True)
                    
    # And finally filter the models:
    if isinstance(model.first(), Texts): # texts table is filtered
        results = model.filter(owner=request.user).\
                        filter(filter_Q_lang).\
                        filter(filter_Q_time).\
                        filter(filter_Q_tag).\
                        filter(filter_Q_archived).\
                        distinct() # because many2many, a text can have 2 tags. don't count 2 times so...
#                         filter(filter_Q_tag).\
    if isinstance(model.first(), Words): # words table is filtered
        results = model.filter(owner=request.user).\
                        filter(filter_Q_lang).\
                        filter(filter_Q_status).\
                        filter(filter_Q_wordtag).\
                        filter(filter_Q_text).\
                        filter(filter_Q_compoundword)
    
    return results

'''useful for javascript for example which sends boolean value 'false' and 'true' for checkbox'''
def str_to_bool(s):
    if s == 'True' or s == 'true':
        return True
    elif s == 'False' or s == 'false':
        return False
    else:
        raise ValueError 

''' clean after uploading the file: remove the file in the dir and the Object'''
def delete_uploadedfiles(filepath, owner):
    os.remove(filepath)
    Restore.objects.filter(owner=owner).delete()

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
    and then insert sentences/words in DB 
    @text  a Text model instance
    @text_txt the text content inside the Text. It's set to something when splitText() on a webpage
    @webpagesection what will be the first webpagesection for the word to add (For 'webpage_read')
    @sentenceorder what will be the order of the first sentence to add (For 'webpage_read')
    @return  the max order of the sentence (used by webpage_read)
'''
def splitText(text, text_t=None, webpagesection=0, sentenceorder=0):
    max_sentenceorder = 0
    
    removeSpaces = text.language.removespaces # Used for Chinese,Jap where the white spaces are not used.
    splitEachChar = text.language.spliteachchar
    splitSentenceMark = text.language.regexpsplitsentences
    noSentenceEnd = text.language.exceptionssplitsentences #"Mr.|Dr.|[A-Z].|Vd.|Vds." 
    termchar = text.language.regexpwordcharacters
    replace = text.language.charactersubstitutions.split("|") # some weird apostrophes are listed, triple dots etc.
    rtlScript = text.language.righttoleft
    ######## PRE-PROCESSING ##############################################################################
    t = text_t if text_t else text.text #the text content inside the Text. It's set to something when splitText() on a webpage
    
    # reverse the text if righttoleft language (like Hebrew/arab) TODO!
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
#         noSentenceEnd = noSentenceEnd.replace('.', '\.') #because the string '\.' were escaped to '.' we need to rescaped them...       t = re.sub(noSentenceEnd , r'‧', t)
        t = re.sub(noSentenceEnd , r'‧', t)

    sentences = splitSentence(t, splitSentenceMark)

    ######################## Splitting and insert sentences/Words in the database ######################
    textOrder = 0
    new_words_created = []
    distinct_wordtext_dict = {} # we´ll count the number of distinct wordtexts (used in text list and in text_read)
    isWord_created_nb = 0 # because bulk_create doesn't return the ID!!!
    for sentTxt in sentences: # Loop on each sentence
        # it will be used to create the 'customsentence': the sentence with the word inside '**...**'
        senttext_before_wo = ''
        senttext_after_wo = ''

        newsentence = Sentences.objects.create(owner=text.owner,language=text.language,
                                               sentencetext=sentTxt, order=sentenceorder,text=text) # create each sentence
        max_sentenceorder = sentenceorder
        sentenceorder += 1
        # splitting the words inside the sentence:
        word_split_pattern = r'([^'+termchar+']+)' # non character are used as the end of word

        sentList = re.split(word_split_pattern, sentTxt) # ['This',' ','is',' ','good','.',' ']
        sentList = [i for i in sentList if i] # remove the empty item created by re.split
        # Special case: it's the delimiter: the '.' at the end of the sentence for ex.
        if len(sentList) > 1 and not re.match(r'[^\W\d_]', sentList[-1]):
            lastitem_isnotword = sentList.pop() 
        else:
            lastitem_isnotword = False
            
        # split each character of each 'word' if it's Japanese/Chinese..
        if splitEachChar: # ..where each character is a word 
            temp_sentList = []
            for wordidx,word in enumerate(sentList): 
                if re.search(r'[' + termchar +  ']', word): # match only word
                    # this regex pattern matches only Japanese/Chinese word.
                    splitEachChar_List = re.split(r'(['+termchar+'])', word)
                    splitEachChar_List = [i for i in splitEachChar_List if i] # remove the empty item created by re.split
                    temp_sentList.extend(splitEachChar_List)
                else: # the element doesn't contain any Jap/Chinese character. not to split in character
                    temp_sentList.append(word)
            sentList = temp_sentList

        for wordidx, word in enumerate(sentList): 
            if re.search(r'[' + termchar +  ']', word): 
                # creating the custom sentence 
                senttext_before_wo = ''.join(sentList[:wordidx])
                senttext_after_wo = ''.join(sentList[wordidx+1:])
                customsentence = senttext_before_wo + '**'+word+'**' + senttext_after_wo

                wo = Words(owner=text.owner,language=text.language, 
                                          sentence=newsentence,text=text,
                                          order=wordidx, textOrder=textOrder,
                                            wordtext=word, customsentence=customsentence, 
#                                               wordtext=remove_spaces(word,removeSpaces), \
                                          webpagesection=webpagesection,
                                          isnotword=False)
                new_words_created.append(wo)
                word_LC = word.lower()
                distinct_wordtext_dict[word_LC] = distinct_wordtext_dict.setdefault(word_LC, 0)+1
                isWord_created_nb += 1
            else: # Non-words
                wo = Words(owner=text.owner,language=text.language, sentence=newsentence,
                                     text=text, order=wordidx, textOrder=textOrder,
                                     wordtext=word, isnotword=True, webpagesection=webpagesection)
                new_words_created.append(wo)
            textOrder += 1
        # Special case: it's the delimiter: the '.' at the end of the sentence for ex.
        if lastitem_isnotword:
            wo = Words(owner=text.owner,language=text.language, sentence=newsentence,text=text,
                             order=wordidx+1, textOrder=textOrder, wordtext=lastitem_isnotword, 
                             isnotword=True, webpagesection=webpagesection)
            new_words_created.append(wo)
    # bulk create words (we can't bulk create sentence since they are used as FK)
    Words.objects.bulk_create(new_words_created)
        
    new_words_created = Words.objects.filter(Q(isnotword=False)&Q(owner=text.owner)).\
                                order_by('-created_date')[:isWord_created_nb]

    ################## SEARCHING THE TEXT FOR SIMILAR WORD: ######################################################
    words_found_similar_to_update = []
    modelwords_to_update = []
    for new_word_created in new_words_created:
        
        # don't process 2 times the same word already processed
        if new_word_created not in words_found_similar_to_update:
            # the word which have a gosw is the model (else, whatever the word)
            samewordtext_query = Words.objects.filter(language=text.language).\
                    filter(wordtext__iexact=new_word_created.wordtext).\
                    order_by('-status')
            # the words found similar must have at least one of them which is a known word
            if samewordtext_query and samewordtext_query.first().status > 0:
                model_word = samewordtext_query.first() #it's used as a model    
                gosw_to_update = model_word.grouper_of_same_words
                # creating a GOSW if needed
                if not gosw_to_update:
                    id_string = json.dumps( [model_word.wordtext, model_word.language.natural_key()])
                    gosw_to_update = Grouper_of_same_words.objects.create(id_string=id_string,
                                                                           owner=text.owner)
                    model_word.grouper_of_same_words = gosw_to_update
                    modelwords_to_update.append(model_word)
                # and update all those words:
                for sameword in samewordtext_query:
                    if sameword in new_words_created:
                        sameword.status = model_word.status
                        sameword.grouper_of_same_words = gosw_to_update
                        sameword.translation = model_word.translation
                        sameword.romanization = model_word.romanization
                        sameword.customsentence = model_word.customsentence
                        words_found_similar_to_update.append(sameword)
    # Bulk update:
    Words.objects.bulk_update(words_found_similar_to_update, ['grouper_of_same_words','status',
                                                              'translation','romanization',
                                                              'customsentence'])
    Words.objects.bulk_update(modelwords_to_update, ['grouper_of_same_words'])
    ################## SEARCHING COMPOUND WORDS: ######################################################
    # loop through all the already known compound words:
    sim_cowo_to_update = []
    for cowo in Words.objects.filter(Q(owner=text.owner)&Q(language=text.language)&\
                                    Q(isCompoundword=True)&Q(isnotword=True)):
        # search sentences containing the compound words
        cowo_wordtext_ls = cowo.wordtext.split('+')
        for idx, cowo_wordtext in enumerate(cowo_wordtext_ls):
            if idx == 0:
                filter_Q_cowo_wordtext = Q(sentencetext__icontains=cowo_wordtext)
            else:
                filter_Q_cowo_wordtext &= Q(sentencetext__icontains=cowo_wordtext)
        cowo_wordtext_sentences = Sentences.objects.filter(text=text).\
                                                    filter(filter_Q_cowo_wordtext)
        # mark the words found in these sentences as compound words:
        # I take the first word written similarly in the sentence.
        # (Maybe need to refine it later???)


        for cowo_wordtext_sentence in cowo_wordtext_sentences:
            notsure_sim_cowo_to_update = []
            bad_sentence = False 
            # the query can find sentences which don't contain the word
            #..in fact: Since the query search for string, not object, it doesn't distinguish
            #.. sentences containing 'do' and 'adorable' when seaarching
            #.. for the wordtext 'do' for example.
            for cowo_wordtext in cowo_wordtext_ls:
                sim_cowo = Words.objects.filter(Q(sentence=cowo_wordtext_sentence)&\
                                                Q(wordtext=cowo_wordtext)).first()
                if not sim_cowo: # the sentence doesn't contain any word with the wordtext
                    bad_sentence = True
                    break
                sim_cowo.isCompoundword = True
                sim_cowo.compoundword = cowo
                sim_cowo.show_compoundword = True
                notsure_sim_cowo_to_update.append(sim_cowo)
            if not bad_sentence:
                sim_cowo_to_update.extend(notsure_sim_cowo_to_update)
    Words.objects.bulk_update(sim_cowo_to_update, ['isCompoundword','compoundword',
                                                   'show_compoundword'])

    # update the wordcount and wordcount without the similar wordtext in the text:
    if text.contenttype == 'html' or text.contenttype == 'doc':
        text.wordcount += isWord_created_nb
        text.wordcount_distinct += len(distinct_wordtext_dict)
    else:
        text.wordcount = isWord_created_nb
        text.wordcount_distinct = len(distinct_wordtext_dict)
    text.save()
    
    return max_sentenceorder

# IS IT USEFUL???
# def remove_spaces(s,remove):
#     ''' some cleaning for the splitting in textitems function '''
#     if remove:
#         return re.sub(r'\s{1,}', r'', s)  
#     else:
#         return s

''' some other cleaning for the splitting in textitems function '''
# def repl_tab_nl(s): NOT USED IN FACT
#     s = re.sub(r'[\r\n\t]', r' ', s)
#     s = re.sub(r'\r\n', r' ', s)
#     s = re.sub(r'\s', r' ', s)
#     s = re.sub(r'\s{2,}', r' ', s)
#     return s.strip()

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

''' CONSTANTS  used inside text_read when displaying the tooltip '''
    #TODO increase the status of learning words each time we open a text that contains this word??
# def get_statuses():
#     statuses = { 0 : {"abbr" :   "0", "name" : _("Unknown")},
#                 1  : {"abbr" :   "1", "name" : _("Learning")},
#                 100 : {"abbr" : _("WKn"), "name" : _("Well Known")},
#                 101 : {"abbr" : _("Ign"), "name" : _("Ignored")}, }
#     return statuses

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
        return _('Learning') #status from 1 to 99
        
''' 
NOTUSEDINFACT
- called by view dictwebpage to create the dict link in text_read bottomright 
- called by pgm.js:  create_link_webdict(wblink1,wblink2,wblink3,txt,txid,torder)
createTheDictLink(wblink1,txt,'Dict1','Lookup Term: ') + =>http://127.0.0.1/trans.php?x=2&i=http%3A//www.wordreference.com/enfr/%23%23%23&t=This  
createTheDictLink(wblink2,txt,'Dict2','') +
createTheDictLink(wblink3,txt,'GTr','') + ...'''
def NOTUSEDINFACTcreateTheDictLink(u,t): 
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



