'''
Moulinette: converting the mysql query to ORM command
/!\ Limitations (voluntary...): * lwt allows to create words, which are absent for the text.
To be consistent, LingL has removed this functionality: I prefer this like that
to not clog the database with words with no reference to text, no id
                                * I didn't search for 'compound word' in other sentences. It's a 
too heavy memory search. 
'''
# second party
import re
import json
# local import
from lwt.models import *
from lwt.views._utilities_views import splitText

data_file = 'lwt/insert_old_lwt/lwt-backup-2017-10-06-08-45-34.sql'

''' helper function for import_oldlwt. 
the glosbe api url is outdated: it was of the form: "glosbe_api.php?from=de&dest=en&phrase=###"
when it should be: "https://glosbe.com/gapi/translate?from=eng&&dest=fra&&format=json" '''
def converter_bad_url(url):
    if 'glosbe' in url:
        from_639_1 = re.search(r'(?<=from=).{2}', url).group()
        dest_639_1 = re.search(r'(?<=dest=).{2}', url).group()
        # the code lang was '639_1' (2 letters) form => it's now '639_2t' (3 letters)
        with open('lwt/fixtures/languages_codes.json') as lang_codes_files:
            lang_codes_json = lang_codes_files.read()
        languages_codes = json.loads(lang_codes_json)
        for lang in languages_codes: 
            if '1' in lang.keys() and lang['1'] == from_639_1:
                from_639_2t = lang['2T']
            if '1' in lang.keys() and lang['1'] == dest_639_1:
                dest_639_2t = lang['2T']
        return "https://glosbe.com/gapi/translate?from="+from_639_2t+"&&dest="+dest_639_2t+"&&format=json"
    else:
        return url

''' data_file: sql file, uncompressed
    owner: request.user
    => from the sql file, create all the tables '''
def import_oldlwt(owner, data_file):
    # dicts where "'old_lwt_id'" :  <Word object in new lwt>
    languages_dict = {}
    texttags_dict = {}
    texts_dict = {}
    wordtags_dict = {}
    words_dict = {}
    knownwords_dict = {} # in this dict, there can be several <Words> for each key
    for line in data_file.readlines():
        line = line.decode()
        # cleaning:
        line = line.replace('\\n','\n') # because Python is always escaping `\n` without reasons...
        line = line.rstrip('\n')
        line = line.replace('\\\'', '\'') # replace \'  => ' (the quote are escaped in the saved created by old lwt
        # Inserting in Languages:
        insertinto_str = 'INSERT INTO languages VALUES('
        if line.startswith(insertinto_str):
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            # because 
            language = Languages.objects.create(
                                            owner = owner,
                                             name = el[1],
                                             dict1uri = converter_bad_url(el[2]),
                                             dict2uri = converter_bad_url(el[3]),
                                             googletranslateuri = converter_bad_url(el[4]),
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
            languages_dict[el[0]] = language

        # Inserting into Texttags
        insertinto_str = 'INSERT INTO tags2 VALUES('
        if line.startswith(insertinto_str):
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            texttag = Texttags.objects.create(
                                            owner = owner,
                                             txtagtext = el[1],
                                             txtagcomment = el[2],
                                     )
            texttags_dict[el[0]] = texttag

        # Inserting into Texts
        insertinto_str = 'INSERT INTO texts VALUES('
        if line.startswith(insertinto_str):
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            text = Texts.objects.create(
                                            owner = owner,
                                             language  = languages_dict[el[1]],
                                             title = el[2],
                                             text = el[3],
                                             annotatedtext = el[4],
                                             audiouri = el[5],
                                             sourceuri = el[6],
                                        #     texttags = models.ManyToManyField(Texttags,related_name='texthavingthistag') 
                                     )
            texts_dict[el[0]] = text
            # create the sentence, and words based upon this text 
            splitText(text)
            
        # adding texttags to the texts:
        insertinto_str = 'INSERT INTO texttags VALUES('
        if line.startswith(insertinto_str):
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            txid = el[0]
            txtagid = el[1]
            texts_dict[txid].texttags.add(texttags_dict[txtagid])
            texts_dict[txid].save()
        
        # Inserting into Wordtags
        insertinto_str = 'INSERT INTO tags VALUES('
        if line.startswith(insertinto_str):
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            wordtag = Wordtags.objects.create(
                                            owner = owner,
                                             wotagtext = el[1],
                                             wotagcomment = el[2],
                                     )
            wordtags_dict[el[0]] = wordtag
            
        # Updating the Words with the old_lwt Words table:
        insertinto_str = 'INSERT INTO words VALUES('
        if line.startswith(insertinto_str):
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            # get the word in the old model
            language = languages_dict[el[1]]
            wordtext = el[2]
            
            def convert_old_status(old_status):
                # we don't use the same numbers for the status than in the old lwt:
                if old_status >= 1 and old_status <= 5:
                    new_status = 1 # learning
                elif old_status == 99:
                    new_status = 100 # well-known
                elif old_status == 98:
                    new_status = 101 # ignored
                return new_status

            def update_word(word, isCompoundword, isnotword, old_lwt_id=None):
                # and update the fields:
                word.isCompoundword = isCompoundword
                word.isnotword = isnotword
                if not isCompoundword or (isCompoundword and isnotword):
                    # updates for Compoundword ForeignKey OR for independend word
                    word.status = convert_old_status(int(el[4]))
                    word.translation = el[5]
                    word.romanization = None if el[6] == 'NULL' else el[6]
                    word.customsentence = el[7].replace('{','**').replace('}','**')
                if isCompoundword and not isnotword:
                    word.show_compoundword = True # I arbitrarily chose to default them to show the compound word
                word.save()
                if not isCompoundword:
                    # for each old lwt id, we associate one or more word in the new lwt
                    knownwords_dict.setdefault(old_lwt_id, []).extend([word])
            # Special case: Compound words:
            # if Chinese/japanse: the word is more than one char
            # else: the word is compound of more than 1 word, separated by space
            # First, get the number of component inside:
            if language.spliteachchar: # Japanese/Chinese
                compoundword_wordtext_list = wordtext
            elif not language.spliteachchar: # non Janpanese/Chinese
                word_match_pattern = r'['+language.regexpwordcharacters+']+' # 'qu\'est-ce que' => 'qu','est','ce'.'que'
                compoundword_wordtext_list = re.findall(word_match_pattern, wordtext)

            artificially_created_by_lwt = False # see the "limitation in the function comment

            # Then, 
            # it IS a compound word
            if len(compoundword_wordtext_list) > 1: 
                wordinside_order_list = []
                wordinside_obj_order_list = []
                for idx,compoundword_wordtext in enumerate(compoundword_wordtext_list):
                    sentencetext = el[7].replace('{','') # used after to get the word (and only this one)
                    sentencetext = sentencetext.replace('}','')
                    # case-insensitive search: for ex because of 'Qu'est-ce que'
                    words = Words.objects.filter(language_id=language.id, 
                                            wordtext__iexact=compoundword_wordtext,
                                            sentence__sentencetext__contains=sentencetext)
                    if not words: # the word has not existence in the text
                        artificially_created_by_lwt = True 
                        break
                    if idx == 0:
                        firstword = words[0] # used after to create the ForeignKey
                    for compoundwo in words: # update all occurences of the same word
                        update_word(compoundwo, isnotword=False, isCompoundword=True, old_lwt_id=el[0])
                        wordinside_order_list.append(compoundwo.id)
                        wordinside_obj_order_list.append(compoundwo)

                wordtext = '+'.join(compoundword_wordtext_list)
                wordinside_order_NK = [[wo.wordtext, wo.language.natural_key()]
                                       for wo in wordinside_obj_order_list]
                wordinside_order_NK = json.dumps(wordinside_order_NK)
                # and create the ForeignKey compoundword:
                if not artificially_created_by_lwt: # the word exists in the text
                    compoundword = Words.objects.create(owner = owner,
                                        language = firstword.language,
                                        wordtext = wordtext,
                                         sentence = firstword.sentence,
                                         text = firstword.text,
                                         wordinside_order = json.dumps(wordinside_order_list, separators=(',',':')),
                                         wordinside_order_NK = wordinside_order_NK
                                         )
#                     # give it a grouper_of_same_word FK with the same id:
#                     grouper_of_same_words = Grouper_of_same_words.objects.create(id=compoundword.id)
#                     compoundword.grouper_of_same_words = grouper_of_same_words
#                     compoundword.save()

                    update_word(compoundword, isCompoundword=True, isnotword=True, old_lwt_id=None)
                    # and insert word_inside_order json format for each word inside as long as the ForeignKey:
                    for wordinside in wordinside_obj_order_list:
                        wordinside.compoundword = compoundword
                        wordinside.show_compoundword = True
                    Words.objects.bulk_update(wordinside_obj_order_list, ['compoundword','show_compoundword'])
                    # and add to the list of known words (it will be a special case, to be processed after
                    old_lwt_id=el[0]
                    knownwords_dict.setdefault(old_lwt_id, []).extend([compoundword])
                    
            # it's not a compound word
            elif len(compoundword_wordtext_list) == 1: 
                    # get all the words written similarly:
                    # it's case insensitive because that's the way in the lwt database: all the word (even not the
                    # LC, have the first char in lowercase!
                    words = Words.objects.filter(language_id=language.id, wordtext__iexact=wordtext).\
                                                        order_by('id')
                    if not words: # the word has not existence in the text
                        artificially_created_by_lwt = True 
                    elif not artificially_created_by_lwt: # the word exists in the text
                        if len(words) > 1: # several words written similarly
                            id_string = json.dumps([words.first().wordtext, words.first().language.natural_key()])
                            gosw = Grouper_of_same_words.objects.create(id_string=id_string,
                                                                                   owner=owner)
                            for wo in words:
                                wo.grouper_of_same_words = gosw
#                             if words[0].grouper_of_same_words.id != words[0].id: # it was already defined elsewhere
#                                 pass
#                             elif words[0].grouper_of_same_words.id == words[0].id:
#                                 grouper_of_same_words = Grouper_of_same_words(id=words[0].id)
#                                 for idx, wo in enumerate(words): # put the same value in all these same words
                                update_word(wo, isCompoundword=False, isnotword=False, 
                                                old_lwt_id=el[0])
#                                     wo.grouper_of_same_words = grouper_of_same_words
                        elif len(words) == 1: # word is alone written like this
                            update_word(words[0], isCompoundword=False, isnotword=False, old_lwt_id=el[0])
            
        # adding wordtags to the words:
        insertinto_str = 'INSERT INTO wordtags VALUES('
        if line.startswith(insertinto_str):
            line = line.lstrip(insertinto_str)
            line = line.rstrip(');')
            el = re.split(r'(?:(?<=\')|(?<=NULL)),(?:(?=\')|(?=NULL))', line)
            el = [e.strip('\'') for e in el] # there's "'field'" for each field. remove the extra ''
            wtwoid = el[0]
            wttgid = el[1]
            for wo in knownwords_dict[wtwoid]:
                wo.wordtags.add(wordtags_dict[wttgid ])
                wo.save()
            