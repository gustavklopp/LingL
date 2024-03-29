'''
Moulinette: converting the mysql query to ORM command
'''
from django.templatetags.static import static # to use the 'static' tag as in the templates
from django.db.models import Q
from django.db.utils import IntegrityError
from django.contrib import messages
from django.utils.translation import ugettext as _
# second party
import re
import json
import csv
import gc
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
        pass
#         from_639_1 = re.search(r'(?<=from=).{2}', url).group()
#         dest_639_1 = re.search(r'(?<=dest=).{2}', url).group()
#         # the code lang was '639_1' (2 letters) form => it's now '639_2t' (3 letters)
#         for lang in LANGUAGES_CODE: 
#             if lang['1'] == from_639_1:
#                 from_639_2t = lang['2T']
#             if lang['1'] == dest_639_1:
#                 dest_639_2t = lang['2T']
#         return "https://glosbe.com/gapi/translate?from="+from_639_2t+"&&dest="+dest_639_2t+"&&format=json"
    elif 'www.dict.cc' in url: # dict.cc is bad formed
        lang_code1 = 'XX'
        for lang in LANGUAGES_CODE:
            if lang['name'] == name:
                lang_code1 =  lang['1']
        return 'http://'+lang_code1+'-'+origin_lang_code+'.syn.dict.cc/?s=<WORD>'
    else:
        return url

def mp_create_wordtag_args(lwt_wordId, lwt_wordtagId, 
#                            words_dict, 
#                            word_created_Objs, 
#                            wordtags_dict, 
#                            wordtag_created_Objs, 
                            args, owner
                           ):
#     print('\ninside multi-process:\nlwt_wordId = {}/ lwt_wordtagId = {}'.format(lwt_wordId, lwt_wordtagId))
    ThroughModel = Words.wordtags.through
    # look for word obj (You can have several word_objects since we include simwo
    word_objs = Words.objects.filter(Q(owner=owner)&Q(oldlwtid=lwt_wordId))
# #     word_obj = words_dict[lwt_wordId]
# #     if isinstance(word_obj, int):
# #         word_obj = word_created_Objs[word_obj]
    # look for wordtag obj
    wordtag_obj = Wordtags.objects.get(owner=owner, oldlwtid=lwt_wordtagId)
# #     wordtag_obj = wordtags_dict[lwt_wordtagId]
# #     if isinstance(wordtag_obj, int):
# #         wordtag_obj = wordtag_created_Objs[wordtag_obj]
    for word_obj in word_objs:
        args.append(ThroughModel(wordtags=wordtag_obj, words=word_obj))

############ LINE_PROFILER ###############
# import line_profiler
# profile = line_profiler.LineProfiler()

''' 
@data_file: sql file, uncompressed
@owner: request.user
@return: a dictionary summarizing the number of elements created '''
# @profile
def import_oldlwt(owner, data_file, request):
    # dicts where "'old_lwt_id'" :  <Word object in new lwt>
    languages_dict = {}
    createdLanguage_nb = 0
    texttags_dict = {}
    texts_dict = {}
#     wordtagID_wordtagObj_dict = {}
#     oldlwtID_wordNK_dict = {} # in this dict, there can be several <Words> for each key
    texttags_to_create = []
    texttags_to_create_idx = 0
    wordtags_to_create = []
    wordtags_to_create_idx = 0
    words_to_create = []
    words_to_create_idx = 0
    words_to_update = []
    wordsWordtags_to_update = {}
    current_operation = '' # are we in the block of inserting text, word, language etc...
    newtext_to_create = []
    newtext_to_create_idx = 0
    text_texttag_dict = {}
#     words_dict = {}
#     wordtags_dict = {}
#     equiv_word_oldlwtid_lingid_to_create = []
#     equiv_wordtag_oldlwtid_lingid_to_create = []


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
                try:
                    Texts.objects.bulk_create(newtext_to_create)
                except IntegrityError:
                    messages.add_message(request, messages.ERROR, _('Import of Texts failed: Duplicate(s) detected (texts with the same title)! You should remove (or rename) duplicate(s) in LWT and backup again.'))
                    return {'createdLanguage_nb':createdLanguage_nb, 'createdText_nb':'DUP', 'createdWord_nb':'DUP'}
                        
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
            current_operation = 'inserting_wordtag'
            line = line.lstrip(insertinto_str)
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
#             wordtagID_wordtagObj_dict[el[0]] = wordtag
            # check whether this wordtag already exists in database
            try:
                wordtag = Wordtags.objects.get(Q(owner=owner)&Q(wotagtext=el[1]))
#                 wordtags_dict[el[0]] = wordtag
            except Wordtags.DoesNotExist:
                wordtag = Wordtags( owner = owner,
                                    wotagtext = el[1],
                                    wotagcomment = el[2],
                                    oldlwtid = el[0])
                wordtags_to_create.append(wordtag)
#                 wordtags_dict[el[0]] = wordtags_to_create_idx
                wordtags_to_create_idx += 1
                
        # Updating the Words with the old_lwt Words table:
        insertinto_str = 'INSERT INTO words VALUES('
        if line.startswith(insertinto_str):
    
            # time to bulk create the wordtags:
            if wordtags_to_create:
                Wordtags.objects.bulk_create(wordtags_to_create)
                # and get the result:
                wordtag_created_Objs = Wordtags.objects.filter(owner=owner).\
                                        order_by('created_date')
                wordtag_created_Objs = wordtag_created_Objs[wordtag_created_Objs.count() - len(wordtags_to_create):]
                wordtags_to_create = [] # we´ll be used later to avoid bulk_creating wordtag again
    
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
    
#             '''used later for editing wordtags by looking for the Natural keys'''
#             def _add_to_wordtag_dict(word):
#                 if word.textOrder:
#                     oldlwtID_wordNK_dict[el[0]] = (word.textOrder, word.text.title, owner.username)
#                 else:
#                     oldlwtID_wordNK_dict[el[0]] = (word.wordtext, word.language.name, owner.username)
    
            # Check whether this word already exists in database.
            # if it exists, we don't create a new word but we choose to OVERWRITE 
            # the data currently present with the ones from oldlwt
            duplicate_word = Words.objects.filter(Q(owner=owner)&Q(language=language)&\
                                               Q(status__gt=0)&Q(wordtextLC=wordtext)).\
                                               order_by('-grouper_of_same_words').first()
            if duplicate_word:
                # we need also to update all the similar words for this word:
                if gosw := duplicate_word.grouper_of_same_words:
                    for simwo in gosw.grouper_of_same_words_for_this_word.all():
                        simwo.status = status
                        simwo.translation = translation
                        simwo.romanization = romanization
                        simwo.customsentence = customsentence
                        simwo.oldlwtid = el[0] 
                        words_to_update.append(simwo)
#                         words_dict[el[0]] = simwo TO DO LATER
                else: # this word has no similar words defined
                    duplicate_word.status = status
                    duplicate_word.translation = translation
                    duplicate_word.romanization = romanization
                    duplicate_word.customsentence = customsentence
                    duplicate_word.oldlwtid = el[0] 
                    words_to_update.append(duplicate_word)
#                     words_dict[el[0]] = duplicate_word TO DO LATER
    
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
                                wordinside_order_NK = wordinside_order_NK,
                                oldlwtid = el[0]
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
                                customsentence = customsentence,
                                oldlwtid = el[0]
                                )
                words_to_create.append(wo)
#                 words_dict[el[0]] = words_to_create_idx
                words_to_create_idx += 1
#                 print(wordtext)
    
#             oldlwtID_wordNK_dict[el[0]] = (wordtext, language.name, owner.username)
                
        # adding wordtags to the words:
        insertinto_str = 'INSERT INTO wordtags VALUES('
        if line.startswith(insertinto_str):
            current_operation = 'inserting_wordtag'
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
    
#             wordsWordtags_to_update.setdefault(oldlwtID_wordNK_dict[el[0]], []).\
#                                                 extend( [wordtagID_wordtagObj_dict[el[1]] ] )
            wordsWordtags_to_update[el[0]] = el[1]
                
#     print('creating words')
    Words.objects.bulk_create(words_to_create)
    # and get back the texts object which was created:
#     word_created_Objs = Words.objects.filter(owner=owner).\
#                             order_by('created_date')
#     word_created_Objs = word_created_Objs[word_created_Objs.count() - len(words_to_create):]
    
#     print('updating words')
    Words.objects.bulk_update(words_to_update, ['status','translation','romanization','customsentence',
                                                'oldlwtid'])
    # update wordtag:
#     print('start of updating wordtags')
#     print('{} wordtag to update'.format(len(wordsWordtags_to_update)))

    # wordsWordtags_to_update is a dict: {'oldlwtID':['wordtagID','wordtagID',...], 'oldlwtID':[....],...}
    # wordsWordtags_to_update is a dict: {'wordNK':['wordtag','wordtag',...], 'wordNK':[....],...}
#     with open('wordsWordtags.txt', 'r') as f:
#         wordsWordtags_to_update = json.loads(f.read())
#  
    
    if wordsWordtags_to_update:
        # and we bulk_insert (called 'bulk_create' with ThroughModel in fact) at this moment for wordtag:
        # using multiprocessing:
        import multiprocessing as mp
        from itertools import repeat
         
        with mp.Manager() as manager:
            # this list and dict will be shared betwen the processes. They need to be converted
            # in a format called 'proxyList' and 'proxyDict' (we'll convert back to normal list and dict later)
      
            # this is the way we can pass arguments. They need to be zipped.
            # the mulitprocess will create process for each element of the list new_words_created.
            # the arguments taken needs to be repeated for each element of the list.
#             print('wordsWordtags_to_update = {}'.format(len(wordsWordtags_to_update))) # 63 856
 
#             print('words_dict = {}'.format(len(words_dict))) # 469 578 
#             print('word_created_Objs = {}'.format(len(word_created_Objs))) # 239
#             print('wordtags_dict = {}'.format(len(wordtags_dict))) # 176 675
#             print('wordtag_created_Objs = {}'.format(len(wordtag_created_Objs))) # 135
            args = manager.list()
 
#             with open('wordsWordtags.txt', 'w') as f:
#                 f.write(json.dumps(wordsWordtags_to_update))
 
#             wordsWordtags_to_update = dict(islice(wordsWordtags_to_update.items(), 1000))
            zipped_args = zip( 
                            wordsWordtags_to_update.keys(),
                               wordsWordtags_to_update.values(), 
#                               repeat(words_dict),
#                               repeat(word_created_Objs), 
#                               repeat(wordtags_dict),
#                               repeat(wordtag_created_Objs),
                            repeat(args),
                            repeat(owner)
                             )
            number_workers = mp.cpu_count()
            with manager.Pool(processes=number_workers) as pool:
#                 print('launching multi-process:')
                pool.starmap(mp_create_wordtag_args, zipped_args)
                
            
#             # non-multiprocessing version
#             for i in zipped_args:
#                 mp_create_wordtag_args(*i)
            args = list(args)
    
#         print('Bulk update of wordtags\n')
        ThroughModel = Words.wordtags.through
        ThroughModel.objects.bulk_create(args)
        
        # and free the memory:
        del args
        gc.collect()
        
 
    # OUTPUT THE LINE_PROFILER
#     with open('output.txt', 'w') as stream:
#         profile.print_stats(stream=stream)

    return {'createdLanguage_nb':createdLanguage_nb, 'createdText_nb':len(texts_dict), 
            'createdWord_nb':len(words_to_create)}
    
''' 
LingQ saves are a CSV file of the form:
    term,sentence,tag1,tag2,tag3.....,hintlanguage,translation
@data_file: csv file
@owner: request.user
@return: a dictionary summarizing the number of elements created '''
def import_lingq(owner, data_file, language):
    wordtags_to_create = []
    words_to_create = []
    wotagtexts_ls = []
    wotagtexts_obj_OR_idx_ls = []
    wordtag_word_dic = {}
    wordtags_to_create_idx = 0
    words_to_create_idx = 0
    words_to_update = []
    csv_reader = csv.reader(data_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        else:
            wordtext = row.pop(0).strip()
            customsentence = row.pop(0).strip()
            translation = row.pop().strip()
            # Check whether it already exist in the database:
            word_in_db = Words.objects.filter(Q(owner=owner)&Q(wordtext=wordtext)&Q(language=language)).first()
            if word_in_db:
                word_in_db.customsentence = customsentence
                word_in_db.translation = translation
                words_to_update.append(word_in_db)
                # and also update the words having the same GOSW:
                if gosw := word_in_db.grouper_of_same_words:
                    for simwo in gosw.grouper_of_same_words_for_this_word:
                        simwo.customsentence = customsentence
                        simwo.translation = translation
                        words_to_update.append(simwo)
                wordIdx_OR_obj = word_in_db
            else:
                word = Words(owner=owner,
                             language=language,
                             wordtext=wordtext,
                             customsentence=customsentence,
                             translation=translation,
                             status=1)
                words_to_create.append(word)
                wordIdx_OR_obj = words_to_create_idx
                words_to_create_idx += 1
            
            
            row.pop() # we don´t use 'hintlanguage'
            # then all the others elements are wordtags in fact
            for wotagtext in row:
                if wotagtext == '':
                    continue
                wotagtext = wotagtext.strip()
                # wordtag not yet processed
                if wotagtext not in wotagtexts_ls:
                    wordtag_in_db = Wordtags.objects.filter(Q(owner=owner)&Q(wotagtext=wotagtext)).first()
                    # Check if it already exists in database
                    if wordtag_in_db: 
                        wordtagIdx_OR_obj = wordtag_in_db
                    else:
                        wordtag = Wordtags(owner=owner, wotagtext = wotagtext)
                        wordtags_to_create.append(wordtag)
                        wordtagIdx_OR_obj = wordtags_to_create_idx
                        wordtags_to_create_idx += 1
                    wotagtexts_ls.append(wotagtext)
                    wotagtexts_obj_OR_idx_ls.append(wordtagIdx_OR_obj)
                else: # wordtag already processed
                    wordtagIdx_OR_obj = wotagtexts_obj_OR_idx_ls[wotagtexts_ls.index(wotagtext)]
                wordtag_word_dic.setdefault(wordtagIdx_OR_obj, []).\
                                            extend([wordIdx_OR_obj])

            
    # bulk update:
    Words.objects.bulk_update(words_to_update, ['translation','customsentence'])
    # bulk creation:
    Wordtags.objects.bulk_create(wordtags_to_create)
    Words.objects.bulk_create((words_to_create))
    # and we get the words created:
    words_created = Words.objects.filter(Q(owner=owner)&Q()).\
                                        order_by('created_date')
    words_created = words_created[words_created.count() - len(words_to_create):]
    # and the wordtags created:
    wordtags_created = Wordtags.objects.filter(Q(owner=owner)&Q()).\
                                        order_by('created_date')
    wordtags_created = wordtags_created[wordtags_created.count() - len(wordtags_to_create):]

    # update the words with the correct wordtags:
    # it is done via the ThroughModel in fact:
    ThroughModel = Words.wordtags.through
    args = []
    for wordtagIdx_OR_obj, wordIdx_OR_obj_ls in wordtag_word_dic.items():
        # look for wordtag obj
        if isinstance(wordtagIdx_OR_obj, int):
            wordtag_obj = wordtags_created[wordtagIdx_OR_obj]
        else:
            wordtag_obj = wordtagIdx_OR_obj
        for wordIdx_OR_obj in wordIdx_OR_obj_ls:
            # look for wordtag obj
            if isinstance(wordIdx_OR_obj, int):
                word_obj = words_created[wordIdx_OR_obj]
            else:
                word_obj = wordIdx_OR_obj
            # only update if the wordtag doesn't exist in this word:
            if wordtag_obj not in word_obj.wordtags.all():
                args.append(ThroughModel(wordtags=wordtag_obj, words=word_obj))
    ThroughModel.objects.bulk_create(args)
    
    return {'createdWord_nb':len(words_to_create)}
        
''' 
Readlang saves are a CSV file of the form:

@data_file: csv file
@owner: request.user
@return: a dictionary summarizing the number of elements created '''
def import_readlang(owner, data_file):
    words_to_create = []
    words_to_update = []
    csv_reader = csv.reader(data_file, delimiter=',')
    line_count = 0
    prev_language_code = ''
    createdLanguage_nb = 0
    for row in csv_reader:
        if line_count == 0:
            if row and 'Your words (csv format)' in row[0]:
                line_count += 1
            continue
        elif line_count < 4:
            line_count += 1
            continue
        else:
            wordtext = row.pop(0).strip()
            language_code = row.pop(0).strip()
            translation = row.pop(0).strip()
            customsentence = row.pop(0).strip()
            # Get the language corresponding to the language code:
            if language_code != prev_language_code:
                language = Languages.objects.filter(Q(owner=owner)&Q(code_639_1=language_code)).first()
                # the language with this code doesn't exist for this use, we check in admin:
                if not language:
                    language = Languages.objects.filter(Q(owner_id=1)&Q(code_639_1=language_code)).first()
                    # make a copy of this language for the User:
                    language.id = None
                    language.owner = owner
                    language.save()
                    createdLanguage_nb += 1
                # still no language. we must create it:
                if not language:
                    language_definition = ''
                    for lang in LANGUAGES_CODE:
                        if lang['1'] == language_code:
                            language_definition = lang
                            break
                    language = Languages.objects.create(owner=owner,
                                         name=language_definition['name'],
                                         code_639_1=language_definition['1'],
                                         code_639_2t=language_definition['2T'],
                                         code_639_2b=language_definition['2B'],
                                         django_code=language_definition['django_code']
                                         )
                    createdLanguage_nb += 1
                prev_language_code = language_code
            
            # Check whether it already exist in the database:
            word_in_db = Words.objects.filter(Q(owner=owner)&Q(wordtext=wordtext)&Q(language=language)).first()
            if word_in_db:
                word_in_db.customsentence = customsentence
                word_in_db.translation = translation
                words_to_update.append(word_in_db)
                # and also update the words having the same GOSW:
                if gosw := word_in_db.grouper_of_same_words:
                    for simwo in gosw.grouper_of_same_words_for_this_word:
                        simwo.customsentence = customsentence
                        simwo.translation = translation
                        words_to_update.append(simwo)
            else:
                word = Words(owner=owner,
                             language=language,
                             wordtext=wordtext,
                             customsentence=customsentence,
                             translation=translation,
                             status=1)
                words_to_create.append(word)
            
    # bulk update:
    Words.objects.bulk_update(words_to_update, ['translation','customsentence'])
    # bulk creation:
    Words.objects.bulk_create((words_to_create))
    
    return {'createdWord_nb':len(words_to_create), 'createdLanguage_nb':createdLanguage_nb}
        