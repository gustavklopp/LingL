'''
Moulinette: converting the mysql query to ORM command
'''
from django.templatetags.static import static # to use the 'static' tag as in the templates
from django.db.models import Q
# second party
import re
import json
# local import
from lwt.models import *
from lwt.constants import  LANGUAGES_CODE

data_file = 'lwt/insert_old_lwt/lwt-backup-2017-10-06-08-45-34.sql'

''' helper function for import_oldlwt. the DICTURI are malformed, need to convert them 
and (But the glosbe api doesn't work anymore in fact) the glosbe api url is outdated: 
it was of the form: "glosbe_api.php?from=de&dest=en&phrase=###"
when it should be: "https://glosbe.com/gapi/translate?from=eng&&dest=fra&&format=json"
@url              the url extracted from the SQL save 
@name             the name of the language. Used because we try to get the good language code
@origin_lang_code it's the code '1' in constants.LANGUAGES_CODE
 '''
def converter_bad_url(url, name, origin_lang_code):
    url = url.replace('###', '<WORD>') # I'm using different placeholder
    if 'glosbe' in url:
        from_639_1 = re.search(r'(?<=from=).{2}', url).group()
        dest_639_1 = re.search(r'(?<=dest=).{2}', url).group()
        # the code lang was '639_1' (2 letters) form => it's now '639_2t' (3 letters)
        for lang in LANGUAGES_CODE: 
            if lang['1'] == from_639_1:
                from_639_2t = lang['2T']
            if lang['1'] == dest_639_1:
                dest_639_2t = lang['2T']
        return "https://glosbe.com/gapi/translate?from="+from_639_2t+"&&dest="+dest_639_2t+"&&format=json"
    elif 'www.dict.cc' in url: # dict.cc is bad formed
        lang_code1 = 'XX'
        for lang in LANGUAGES_CODE:
            if lang['name'] == name:
                lang_code1 =  lang['1']
        return 'http://'+lang_code1+'-'+origin_lang_code+'.syn.dict.cc/?s=<WORD>'
    else:
        return url

############ LINE_PROFILER ###############
# import line_profiler
# profile = line_profiler.LineProfiler()

''' @data_file: sql file, uncompressed
@owner: request.user
@return: None => from the sql file, create all the tables '''
# @profile
def import_oldlwt(owner, data_file):
    # dicts where "'old_lwt_id'" :  <Word object in new lwt>
    languages_dict = {}
    createdLanguage_nb = 0
    texttags_dict = {}
    texts_dict = {}
    wordtagID_wordtagObj_dict = {}
    oldlwtID_wordNK_dict = {} # in this dict, there can be several <Words> for each key
    texttags_to_create = []
    texttags_to_create_idx = 0
    words_to_create = []
    words_to_update = []
    wordsWordtags_to_update = {}
    current_operation = '' # are we in the block of inserting text, word, language etc...
    newtext_to_create = []
    newtext_to_create_idx = 0
    text_texttag_dict = {}
    for line in data_file.readlines():
        line = line.decode()
        # cleaning:
        line = line.replace('\\n','\n') # because Python is always escaping `\n` without reasons...
        line = line.rstrip('\n')
        line = line.replace('\\\'', '\'') # replace \'  => ' (the quote are escaped in the saved created by old lwt
        # Inserting in Languages:
        insertinto_str = 'INSERT INTO languages VALUES('
        if line.startswith(insertinto_str):
            current_operation = 'inserting_language'
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            # check whether this language already exists in database
            try:
                language = Languages.objects.get(Q(owner=owner)&Q(name=el[1]))
            except Languages.DoesNotExist:
                language = Languages.objects.create(
                                                owner = owner,
                                                 name = el[1],
                                                 dict1uri = converter_bad_url(el[2], el[1], owner.origin_lang_code),
                                                 dict2uri = converter_bad_url(el[3], el[1], owner.origin_lang_code),
                                                 googletranslateuri = converter_bad_url(el[4], el[1], owner.origin_lang_code),
    #                                              exporttemplate = el[5],
                                                 textsize = el[6],
                                                 charactersubstitutions = el[7],
                                                 regexpsplitsentences = el[8],
                                                 exceptionssplitsentences = el[9],
                                                 regexpwordcharacters = re.sub(r'\\x{([0-9A-Z]+)\}', \
                                                        lambda a: chr(ord(chr(int(a.group(1), 16)))), el[10]),
                                                 # because for Hebrew for ex.: regexpwordcharacters = '\\x{0590}-\\x{05FF}'
                                                 # when we want: regexpwordcharacters = '\u0590-\u05FF'
                                                 removespaces = int(el[11]),
                                                 spliteachchar = int(el[12]),
                                                 righttoleft = int(el[13])
                                         )
                createdLanguage_nb += 1
            languages_dict[el[0]] = language

        # First we create the texttags. 
        # (The relation between text and texttag will be set later)
        insertinto_str = 'INSERT INTO tags2 VALUES('
        if line.startswith(insertinto_str):
            current_operation = 'creating_texttag'
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            # check whether this texttag already exists in database
            try:
                texttag = Texttags.objects.get(Q(owner=owner)&Q(txtagtext=el[1]))
                texttags_dict[el[0]] = texttag
            except Texttags.DoesNotExist:
                texttag = Texttags( owner = owner,
                                    txtagtext = el[1],
                                    txtagcomment = el[2])
                texttags_to_create.append(texttag)
                texttags_dict[el[0]] = texttags_to_create_idx
                texttags_to_create_idx += 1

        # Inserting into Texts. Texts are archived by default
        insertinto_str = 'INSERT INTO texts VALUES('
        if line.startswith(insertinto_str):

            # time to bulk create the texttags:
            if texttags_to_create and current_operation == 'creating_texttag':
                Texttags.objects.bulk_create(texttags_to_create)
                # and get the result:
                texttag_created_Objs = Texttags.objects.filter(owner=owner).\
                                        order_by('created_date')
                texttag_created_Objs = texttag_created_Objs[texttag_created_Objs.count() - len(texttags_to_create):]
                
            current_operation = 'inserting_text'
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            try: # change name if the text already exists with this title
                text = Texts.objects.get(owner=owner, title=el[2])
                el[2] = text.title + ' (2)'
                texts_dict[el[0]] = text
            except:
                text = Texts(owner = owner,
                             language  = languages_dict[el[1]],
                             title = el[2],
                             text = el[3],
                             annotatedtext = el[4],
                             audiouri = el[5],
                             sourceuri = el[6],
                        #     texttags = models.ManyToManyField(Texttags,related_name='texthavingthistag') 
                             archived = True
                             )
                newtext_to_create.append(text)
                texts_dict[el[0]] = newtext_to_create_idx
                newtext_to_create_idx += 1
            
        # adding texttags to the texts (the texttags have been bulk_created previously):
        insertinto_str = 'INSERT INTO texttags VALUES('
        if line.startswith(insertinto_str):

            # Time to bulk create the texts from the previous reading
            # (but we'll in any case bulk_create the texts with another inserting block if there's no texttag)
            if current_operation == 'inserting_text':
                Texts.objects.bulk_create(newtext_to_create)
                current_operation = 'inserting texttag'
                # and get back the texts object which was created:
                text_created_Objs = Texts.objects.filter(owner=owner).\
                                        order_by('created_date')
                text_created_Objs = text_created_Objs[text_created_Objs.count() - len(newtext_to_create):]
                newtext_to_create = [] # we´ll be used later to avoid bulk_creating text again

            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            txid = el[0]
            txtagid = el[1]
            # relation between the index (in LWT) of the text and the texttag:
            text_texttag_dict[txid] = txtagid
            # we can´t  directly use texts_dict[txid] to get the text because bulk_create doesn't associate it with an id
#             textObjORidx = texts_dict[txid]
#             if isinstance(textObjORidx, int):
#                 txttag_to_update_text = text_created_Objs[textObjORidx]
#                 texts_dict[txid] = txttag_to_update_text
#             else:
#                 txttag_to_update_text = textObjORidx
#             txttag_to_update_text = Texts.objects.get_by_natural_key(*(texts_dict[txid]))
#             txttag_to_update_text.texttags.add(texttags_dict[txtagid])
#             txttag_to_update_text.save()
#             texts_dict[txid].save()
        
        # Inserting into Wordtags
        insertinto_str = 'INSERT INTO tags VALUES('
        if line.startswith(insertinto_str):
            current_operation = 'inserting_tag'
            line = line.lstrip(insertinto_str)
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            try: # check duplicate
                wordtag = Wordtags.objects.get(owner=owner, wotagtext__iexact=el[1])
            except Wordtags.DoesNotExist:
                wordtag = Wordtags.objects.create(
                                                owner = owner,
                                                 wotagtext = el[1],
                                                 wotagcomment = el[2],
                                         )
            wordtagID_wordtagObj_dict[el[0]] = wordtag
            
        # Updating the Words with the old_lwt Words table:
        insertinto_str = 'INSERT INTO words VALUES('
        if line.startswith(insertinto_str):

            # we bulk_create the texts with another inserting block 
            # if it wasn't done before already (if there's not texttag for ex.)
            if newtext_to_create:
                Texts.objects.bulk_create(newtext_to_create)
                
            if text_texttag_dict:
                # and we bulk_insert (called 'bulk_create' with ThroughModel in fact) at this moment for texttag:
                ThroughModel = Texts.texttags.through
                args = []
                for lwt_textId, lwt_texttagId in text_texttag_dict.items():
                    # look for text obj
                    text_obj = texts_dict[lwt_textId]
                    if isinstance(text_obj, int):
                        text_obj = text_created_Objs[text_obj]
                    # look for texttag obj
                    texttag_obj = texttags_dict[lwt_texttagId]
                    if isinstance(texttag_obj, int):
                        texttag_obj = texttag_created_Objs[texttag_obj]
                    args.append(ThroughModel(texttags=texttag_obj, texts=text_obj))
                ThroughModel.objects.bulk_create(args)
                text_texttag_dict = {} # prevent trying to bulk_update several times

            current_operation = 'inserting_word'
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            # get the word in the old model
            language = languages_dict[el[1]]
            wordtext = el[2]
            
            ''' we don't use the same numbers for the status than in the old lwt:'''
            def convert_old_status(old_status):
                if old_status >= 1 and old_status <= 5:
                    new_status = 1 # learning
                elif old_status == 99:
                    new_status = 100 # well-known
                elif old_status == 98:
                    new_status = 101 # ignored
                return new_status

            # Special case: Compound words:
            # if Chinese/japanse: the word is more than one char
            # else: the word is compound of more than 1 word, separated by space
            # First, get the number of component inside:
            if language.spliteachchar: # Japanese/Chinese
                compoundword_wordtext_list = wordtext
            elif not language.spliteachchar: # non Japanese/Chinese
                word_match_pattern = r'['+language.regexpwordcharacters+']+' # 'qu\'est-ce que' => 'qu','est','ce'.'que'
                compoundword_wordtext_list = re.findall(word_match_pattern, wordtext)

            status = convert_old_status(int(el[4]))
            translation = None if el[5] == 'NULL' else el[5]
            romanization = None if el[6] == 'NULL' else el[6]
            customsentence = None if el[7] == 'NULL' else el[7].replace('{','**').replace('}','**')

            '''used later for editing wordtags by looking for the Natural keys'''
            def _add_to_wordtag_dict(word):
                if word.textOrder:
                    oldlwtID_wordNK_dict[el[0]] = (word.textOrder, word.text.title, owner.username)
                else:
                    oldlwtID_wordNK_dict[el[0]] = (word.wordtext, word.language.name, owner.username)

            # Check whether this word already exists in database.
            # if it exists, we don't create a new word but we choose to OVERWRITE 
            # the data currently present with the ones from oldlwt
            duplicate_word = Words.objects.filter(Q(owner=owner)&Q(language=language)&\
                                               Q(status__gt=0)&Q(wordtext__iexact=wordtext)).\
                                               order_by('-grouper_of_same_words').first()
            if duplicate_word:
                # we need also to update all the similar words for this word:
                if gosw := duplicate_word.grouper_of_same_words:
                    for simwo in gosw.grouper_of_same_words_for_this_word.all():
                        simwo.status = status
                        simwo.translation = translation
                        simwo.romanization = romanization
                        simwo.customsentence = customsentence
                        words_to_update.append(simwo)
                        _add_to_wordtag_dict(simwo)
                else: # this word has no similar words defined
                    duplicate_word.status = status
                    duplicate_word.translation = translation
                    duplicate_word.romanization = romanization
                    duplicate_word.customsentence = customsentence
                    words_to_update.append(duplicate_word)
                    _add_to_wordtag_dict(duplicate_word)

            else:
                # it IS a compound word
                if len(compoundword_wordtext_list) > 1: 
                    wordtext = '+'.join(compoundword_wordtext_list)
                    wordinside_order_NK = [ [wordtext,language.name,owner.username] 
                                                    for wordtext in compoundword_wordtext_list]
                    wo = Words(owner = owner,
                                language = language,
                                wordtext = wordtext,
                                text = None,
                                isCompoundword=True,
                                isnotword=True,
                                status = status,
                                translation = translation,
                                romanization = romanization,
                                customsentence = customsentence,
                                wordinside_order_NK = wordinside_order_NK
                                )
                        
                # it's not a compound word
                elif len(compoundword_wordtext_list) == 1: 
                    wo = Words(owner = owner,
                                language = language,
                                wordtext = wordtext,
                                text = None,
                                isCompoundword=False,
                                isnotword=False,
                                status = status,
                                translation = translation,
                                romanization = romanization,
                                customsentence = customsentence
                                )
                words_to_create.append(wo)
                _add_to_wordtag_dict(wo)

#             oldlwtID_wordNK_dict[el[0]] = (wordtext, language.name, owner.username)
            
        # adding wordtags to the words:
        insertinto_str = 'INSERT INTO wordtags VALUES('
        if line.startswith(insertinto_str):
            current_operation = 'inserting_wordtag'
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''

            wordsWordtags_to_update.setdefault(oldlwtID_wordNK_dict[el[0]], []).\
                                                extend( [wordtagID_wordtagObj_dict[el[1]] ] )
            
    Words.objects.bulk_create(words_to_create)
    Words.objects.bulk_update(words_to_update, ['status','translation','romanization','customsentence'])
    # update wordtag:
    for wordNK in wordsWordtags_to_update:
        wo = Words.objects.get_by_natural_key(*wordNK)
        for wordtag in wordsWordtags_to_update[wordNK]:
            wo.wordtags.add(wordtag)
        wo.save()

    # OUTPUT THE LINE_PROFILER
#     with open('output.txt', 'w') as stream:
#         profile.print_stats(stream=stream)

    return {'createdLanguage_nb':createdLanguage_nb, 'createdText_nb':len(texts_dict), 
            'createdWord_nb':len(words_to_create)}
        