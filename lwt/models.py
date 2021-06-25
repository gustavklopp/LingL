"""
The original models in lwt:
-archivedtexts
-archtexttags
-languages
-sentences
-settings

-words
-tags
-wordtags : relation table betwwen words and wordtags
            WtWoID: words'ID,   WtTgID: tags ID

-texts:     TxID: texts's ID
-tags2 (T2): texts's tags  T2ID: pk /T2Text: name/T2Comment 
-texttags (Tt): Relation table between texts and tags2    
            TtTxID: texts ID,  TtT2ID: tags2 ID

-textitems
-_lwtgeneral
"""
# django import
from django.db import models
from django.utils import timezone, timesince
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.core import serializers
from django.templatetags.static import static # to use the 'static' tag as in the templates
# second party
# third party
from allauth.account.adapter import DefaultAccountAdapter
# local
from lwt.constants import STATUS_CHOICES, LANGUAGES_CODE

# class FilterByUser_Manager(models.Manager):
# 
#     def get_queryset(self, owner=None):
#         if owner == None:
#             return super(FilterByUser_Manager, self).get_queryset()
#         else:
#             return super(FilterByUser_Manager, self).get_queryset().filter(owner=owner)

class MyUserManager(UserManager): # for deserialization
    def get_by_natural_key(self, username):
        return self.get(username=username)

''' overrding default User to add complementary data '''
class MyUser(AbstractUser):
    # the language that the User already knows: (code is a 2 letters)
    # this 2 letter code is obtained from constants.LANGUAGES_CODE['1'] 
    # (NB: it's NOT LANGUAGES_CODE['django_code'] since it could be a problem when creating
    # dicturi (for example with Chinese since Django_code is 'zh-hans')
    origin_lang_code = models.CharField(max_length=40)
    #is_subscribed = models.BooleanField(default=False)

    objects = MyUserManager() # use to call the parent foreign key by its name (or title , or etc...)

    def __str__(self):
        return self.username 

    def natural_key(self): # For serialization
        return ([self.username])  # I don´t know why but it needs to be put in a list (else, there's an error when loaddata)      
    

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=False) # each user has his own set of the database

#    # You need to redefine save: without it, the password is saved in plain text!
#     def save(self, commit=True):
#         user = super(MyForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user

    class Meta:
        abstract = True


class Extra_field_key(BaseModel):
    title = models.CharField(max_length=20)  

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'extra_field_key'
        unique_together = [['title', 'owner']]


class LanguagesManager(models.Manager):
    def get_by_natural_key(self, name, owner):
        return self.get(name=name, owner__username=owner)
        
class Languages(BaseModel):
    name = models.CharField(max_length=40)  
    dicturi = models.TextField(
                    default="https://glosbe.com/gapi/translate?from=eng&&dest=•••&&format=json, "+\
                            "https://en.wiktionary.org/wiki/###")  
    dict1uri = models.CharField(max_length=200, blank=True, null=True) 
    # for ex: English => French   default="https://glosbe.com/gapi/translate?from=eng&dest=fra&format=json")  
    dict2uri = models.CharField(max_length=200, blank=True, null=True)
    googletranslateuri = models.CharField(max_length=200, blank=True, null=True, 
                    default="*http://translate.google.com/?ie=UTF-8&sl=en&tl=••&text=###")  
    exporttemplate = models.CharField(max_length=1000, blank=True, null=True, 
            default='$status<br>$language<br>$text<br><h1>$word</h1>\t<h1>$translation</h1>'+\
                    '<br>$romanization<br>$sentence<br>$customsentence<br>$compoundword<br>'+\
                    '$similarword\<br>$extrafieldn')
    textsize = models.IntegerField( default=150)  
    charactersubstitutions = models.CharField(max_length=500, default="´='|`='|’='|‘='|...=…|..=‥")  
    regexpsplitsentences = models.CharField(max_length=500, default=".!?:;")  
    exceptionssplitsentences = models.CharField(max_length=500, default="(?<=Mr)\.|(?<=Dr)\.|(?<=[A-Z])\.|(?<=Vd)\.|(?<=Vds)\.")  
    regexpwordcharacters = models.CharField(max_length=500, default="a-zA-ZÀ-ÖØ-öø-ȳ")  
    removespaces = models.BooleanField(default=False)  
    spliteachchar = models.BooleanField(default=False)  
    righttoleft = models.BooleanField(default=False)  
    has_romanization = models.BooleanField(default=False)  
    code_639_1 = models.CharField(max_length=2, blank=True, null=True) # code for the language, 2 letters
    code_639_2t =  models.CharField(max_length=3, blank=True, null=True) # code for the language, 3 letters
    code_639_2b =  models.CharField(max_length=3, blank=True, null=True) # code for the language, 3 letters in English
    django_code =  models.CharField(max_length=8, blank=True, null=True) # code for the language, 3 letters in English
    # JSON List of string. the language model stores only the keys for the extra_field JSON of Words
    extra_field_key = models.ManyToManyField(Extra_field_key, related_name='languagehavingthisextrafieldkey') 

    objects = LanguagesManager() # use to call the parent foreign key by its name (or title , or etc...)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'languages'
        unique_together = [['name', 'owner']]

    def natural_key(self):
        return (self.name, self.owner.username)
        
class TexttagsManager(models.Manager):
    def get_by_natural_key(self, txtagtext, owner):
        return self.get(txtagtext=txtagtext, owner__username=owner)

class Texttags(BaseModel):
    txtagtext = models.CharField(max_length=20)  
    txtagcomment = models.CharField( max_length=200, default='')  

    objects = TexttagsManager() # use to call the parent foreign key by its name (or title , or etc...)

    def __str__(self):
        return self.txtagtext
        
    class Meta:
        db_table = 'texttags'
        unique_together = [['txtagtext', 'owner']]

    def natural_key(self):
        return (self.txtagtext, self.owner.username)
        

class TextsManager(models.Manager):
    def get_by_natural_key(self, title, owner):
        return self.get(title=title, owner__username=owner)
        
class Texts(BaseModel):
    ''' to be deleted, you need to delete the textitem and the sentence containing foreignkey to the text before'''
    language = models.ForeignKey(Languages, related_name='texthavingthislanguage', 
                        on_delete=models.CASCADE) 
    title = models.CharField( max_length=200)  
    text = models.TextField()  
    annotatedtext = models.TextField()  
    audiouri = models.CharField( max_length=200, blank=True, null=True)  
    sourceuri = models.CharField( max_length=1000, blank=True, null=True)  
    #  Link to the Tags
    texttags = models.ManyToManyField(Texttags,related_name='texthavingthistag') 
    lastopentime = models.DateTimeField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    wordcount = models.IntegerField(default=0, blank=True, null=True)
    wordcount_distinct = models.IntegerField(default=0, blank=True, null=True) # same as 'wordcount' but without written similarly word
    CONTENTTYPE_CHOICES = [
        ('text', 'text'),
        ('pdf', 'pdf'),
        ('html', 'html')
    ]
    contenttype = models.CharField(max_length=4, choices=CONTENTTYPE_CHOICES, default='text')

    objects = TextsManager() # use to call the parent foreign key by its name (or title , or etc...)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'texts'
        unique_together = [['title', 'owner']]

    def natural_key(self):
        return (self.title, self.owner.username)

        
class SentencesManager(models.Manager):
    def get_by_natural_key(self, text, order, owner):
        return self.get(text__title=text, order=order, owner__username=owner)

class Sentences(BaseModel): # the Text is cut into sentences
    language = models.ForeignKey(Languages, on_delete=models.CASCADE)
    text = models.ForeignKey(Texts, 
                    on_delete=models.CASCADE) #don't automatically delete words when delete a sentence
    order = models.IntegerField()  # the ordinal number of the sentence in each text
    sentencetext = models.TextField(blank=True, null=True)

    objects = SentencesManager() # use to call the parent foreign key by its name (or title , or etc...)

    def __str__(self):
        return self.sentencetext

    class Meta:
        db_table = 'sentences'
        unique_together = [['text', 'order', 'owner']]

    def natural_key(self):
        return (self.text.title, self.order, self.owner.username)

        
class WordtagsManager(models.Manager):
    def get_by_natural_key(self, wotagtext, owner):
        return self.get(wotagtext=wotagtext, owner__username=owner)

class Wordtags(BaseModel):

    wotagtext = models.CharField(max_length=20)  
    wotagcomment = models.CharField( max_length=200)  

    objects = WordtagsManager() # use to call the parent foreign key by its name (or title , or etc...)

    def __str__(self):
        return self.wotagtext

    class Meta:
        db_table = 'wordtags'
        unique_together = [['wotagtext', 'owner']]

    def natural_key(self):
        return (self.wotagtext, self.owner.username)


class Grouper_of_sameWordsManager(models.Manager):
    def get_by_natural_key(self, id_string):
        return self.get(id_string=id_string)

class Grouper_of_same_words(BaseModel):
    ''' - words written similarly in differents sentences, text... BUT ALSO
        - words written differently, because decided by the User to be similar (for ex. because
        it's a conjugation version of a word like in English: 'write', 'written', 'wrote' etc... )
    
    If detecting, among the saved words, a word (or a compound word) similar to another, we create
    a FK Grouper_of_same_words, linking to the first occurence of the word in question. 
    for ex:  Grouper_of_same_words     id          
                                    NOTHING
            ---------------------------------------------------
             Words    FK GOSW          id           wordtext
                        None          12           'write'  (already SAVED WORD)
                        None          13           'test'   (already SAVED WORD)
                        None          14           'wrote' ==> NEW SAVED WORD

     =>  After recognizing that it´s the same word in fact:
             Grouper_of_same_words     id            
                 FK ['write',Lang]     12          'write'  => Create a new FK
                                       13          'test' 
                 FK ['write',Lang]     14          'wrote'  => Create a new FK

    When a word A is written the same as a word B:
            - create a new FK pointing to word B
          - create the FK in word B to point to the same Grouper_of_same_words as that of word A.
'''
#     id = models.IntegerField(primary_key=True) # not automatic PK because we'll set it to the same as the id for Words
    # words can be looks similar but in fact have different meaning:
    # say we have: fall: autumn OR to fall. LingL will make all this word as similar: not too problematic
    # the problem is if you´ve got another words that you want to make it similar to ´fall´:
    # ´fallen´: will display then ´to fall/ autumn´ in its definition. so we must separate different
    # similar words. Maybe with ´translation´ field? GOSW fall/fallen/fell : FK in fall, transl: ´to lose´
    
    # same than field 'id' but here we keep the 'natural_key' of the word. Used when creating...
    # ... backup and importing backup
    id_string = models.CharField( max_length=500,  unique=True)  

    objects = Grouper_of_sameWordsManager() # use to call the parent foreign key by its name (or title , or etc...)

    class Meta:
        db_table = 'Grouper_of_same_words'

    def natural_key(self):
        return ([self.id_string]) 


class WordsManager(models.Manager):
#     def get_by_natural_key(self, wordtext, textOrder, text, owner):
#         return self.get(wordtext=wordtext, textOrder=textOrder, text__title=text, owner__username=owner)
    def get_by_natural_key(self,  textOrder_OR_wordtext, text_OR_language, owner):
        if type(textOrder_OR_wordtext) == int: 
            return self.get( textOrder=textOrder_OR_wordtext, text__title=text_OR_language, owner__username=owner)
        else: # Word can exist even when the text has been deleted
            return self.get( wordtext=textOrder_OR_wordtext, language__name=text_OR_language, owner__username=owner)

class Words(BaseModel):
    ####      Foreign keys    ####
    language = models.ForeignKey(Languages,blank=True, null=True, related_name='wordhavingthislanguage', 
                                    on_delete=models.CASCADE )
    text = models.ForeignKey(Texts, on_delete=models.SET_NULL, blank=True, null=True, related_name='texthavingthisword')
    sentence = models.ForeignKey(Sentences, related_name='sentence_having_this_word',blank=True, 
                                 null=True, on_delete=models.SET_NULL)
    # compoundword: Several words which together have a meaning in the language:
    # in English: 'turn' and 'off', 'get'and 'up'. or even expression longer
    # we store a ForeignKey on the Words model itself. It takes some extra place in the models but
    # usually User won't create a lot of them...
    # for example: 'white' 'paper' is different from 'paper' 'white'. so store the order of the words
    # a compoundword 'il+y+a':                  isCompoundword=True  isnotword=True
    #  words inside compound word 'il','y','a': isCompoundword=True  isnotword=False
    compoundword = models.ForeignKey('self', blank=True, null=True, \
                       related_name='compoundwordhavingthiswordinside',\
                       on_delete=models.SET_NULL
                       ) # foreignkey to the same table
    grouper_of_same_words = models.ForeignKey(Grouper_of_same_words, null=True, related_name='grouper_of_same_words_for_this_word',
                                              on_delete=models.SET_NULL)
    # Link to the Tags
    wordtags = models.ManyToManyField(Wordtags, related_name='wordtag_with_this_word')

    ####   Not foreign keys  ####
#     STATUS_CHOICES = ( (0, _('Unknown')),
#                        (1, _('Learning')),
#                        (100, _('Well-known')),
#                        (101, _('Ignored')))
    status = models.IntegerField(default=0)  
    order = models.IntegerField(blank=True, null=True)  # where is the word in the sentence
    textOrder = models.IntegerField(blank=True, null=True)  # where is the word in the text
    wordtext = models.CharField( max_length=250,blank=True, null=True)  
    isnotword = models.BooleanField(default=False)  
    translation = models.CharField( max_length=500, blank=True, null=True)  
    romanization = models.CharField( max_length=100, blank=True, null=True)  
    customsentence = models.CharField( max_length=1000, blank=True, null=True) 
    wordinside_order = models.TextField(max_length=250,blank=True,null=True) # stored by dumping JSON format into str
    # same as above but using Natural Key (better than number to import data)
    wordinside_order_NK = models.TextField(max_length=250,blank=True,null=True)
    isCompoundword = models.BooleanField(default=False)
    show_compoundword = models.BooleanField(default=False) # showing compoundword or single word in text_read
    state = models.BooleanField(default=False) # used to export2anki and selectivebackup checkox
    extra_field = models.TextField(max_length=500, blank=True, null=True) # additional, custom field. stored in json format a dict
    webpagesection = models.IntegerField(default=0)

    objects = WordsManager() # use to call the parent foreign key by its name (or title , or etc...)

    def __str__(self):
        return self.wordtext
    
    class Meta:
        db_table = 'words'        
#         unique_together = [['textOrder', 'text', 'owner']] <-- Pb when deleting a word when doing bulk_update

#     def natural_key(self):
#         return (self.wordtext, self.textOrder, self.text.title, self.owner.username)
    def natural_key(self):
        if self.text: 
            return ( self.textOrder, self.text.title, self.owner.username)
        else: # Word can exist even when the text has been deleted:
            return(self.wordtext, self.language.name, self.owner.username)
#####################################################
#             DATABASE 'settings':                  #
#####################################################
class Settings(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    stvalue = models.CharField(blank=True,  max_length=40, null=True) # value chosen by the user
    stdft = models.CharField(blank=True,  max_length=40, default="") # default value
    min = models.IntegerField( null=True) # min value allowed for the user
    max = models.IntegerField(null=True) # max value allowed for the user
    isinteger = models.BooleanField(default='False')

#     objects = FilterByUser_Manager() # overrriding the model Manager to filter by the user requesting the query

    class Meta:
        abstract = True

class Settings_origin_language(Settings):
    pass

class Settings_text_h_frameheight_no_audio(Settings):
    stdft = models.IntegerField(default=140)
    min = models.IntegerField(default=10)
    max = models.IntegerField(default=999)
    isinteger = models.BooleanField(default='True')

    
class Settings_text_h_frameheight_with_audio(Settings):
    stdft= models.IntegerField(default=200)
    min= models.IntegerField(default=10)
    max= models.IntegerField(default=999)
    isinteger = models.BooleanField(default='True')


class Settings_text_l_framewidth_percent(Settings):
    stdft= models.IntegerField(default=50)
    min= models.IntegerField(default=5)
    max= models.IntegerField(default=95)
    isinteger= models.BooleanField(default=True)


class Settings_text_r_frameheight_percent(Settings):
    stdft= models.IntegerField(default=50)
    min= models.IntegerField(default=5)
    max= models.IntegerField(default=95)
    isinteger= models.BooleanField(default=True)


class Settings_test_h_frameheight(Settings):
    stdft= models.IntegerField(default=140)
    min= models.IntegerField(default=10)
    max= models.IntegerField(default=999)
    isinteger = models.BooleanField(default=True)


class Settings_test_l_framewidth_percent(Settings):
    stdft= models.IntegerField(default=50)
    min= models.IntegerField(default=5)
    max= models.IntegerField(default=95)
    isinteger= models.BooleanField(default=True)
    
    
class Settings_test_r_frameheight_percent(Settings):
    stdft= models.IntegerField(default=50)
    min= models.IntegerField(default=5)
    max= models.IntegerField(default=95)
    isinteger= models.BooleanField(default=True)
    
    
class Settings_test_main_frame_waiting_time(Settings):
    stdft= models.IntegerField(default=0)
    min= models.IntegerField(default=0)
    max= models.IntegerField(default=9999)
    isinteger= models.BooleanField(default=True)
    
    
class Settings_test_edit_frame_waiting_time(Settings):
    stdft= models.IntegerField(default=500)
    min= models.IntegerField(default=0)
    max= models.IntegerField(default=99999999)
    isinteger= models.BooleanField(default=True)
    
    
class Settings_test_sentence_count(Settings):
    stdft= models.IntegerField(default=1)
    isinteger= models.BooleanField(default=True)
   
   
class Settings_term_sentence_count(Settings):
    stdft= models.IntegerField(default=1)
    isinteger= models.BooleanField(default=True)
   
    
class Settings_texts_per_page(Settings):
    stdft= models.IntegerField(default=10)
    min= models.IntegerField(default=1)
    max= models.IntegerField(default=9999)
    isinteger= models.BooleanField(default=True)
    
    
class Settings_terms_per_page(Settings):
    stdft= models.IntegerField(default=100)
    min= models.IntegerField(default=1)
    max= models.IntegerField(default=9999)
    isinteger= models.BooleanField(default=True)
    
    
class Settings_tags_per_page(Settings):
    stdft= models.IntegerField(default=100)
    min= models.IntegerField(default=1)
    max= models.IntegerField(default=9999)
    isinteger= models.BooleanField(default=True)
    
    
class Settings_show_all_words(Settings):
    stdft= models.IntegerField(default=0)
    isinteger= models.BooleanField(default=True)
   
   
class Settings_show_text_word_counts(Settings):
    stdft= models.IntegerField(default=1)
    isinteger= models.BooleanField(default=True)
   
   
class Settings_text_visit_statuses_via_key(Settings):
    stdft= models.IntegerField(default=0)
    isinteger= models.BooleanField(default=True)
   
   
class Settings_term_translation_delimiters(Settings):
    stdft= models.CharField(max_length=40, default='/;|')


class Settings_mobile_display_mode(Settings):
    stdft= models.IntegerField(default=0)
    isinteger= models.BooleanField(default=True)
   
   
class Settings_similar_terms_count(Settings):
    stdft= models.IntegerField(default=0)
    min= models.IntegerField(default=0)
    max= models.IntegerField(default=9)
    isinteger= models.BooleanField(default=True)
    
    
# current settings. We'll store them in cookies preferentially but keep them also 
# in database (if cookies are erased for example, we'll still have these data)

''' the language the User is currently learning'''
class Settings_currentlang_name(Settings):
    pass
''' the language the User is currently learning'''
class Settings_currentlang_id(Settings):
    isinteger= models.BooleanField(default=True)


class Settings_currenttext_id(Settings):
    isinteger= models.BooleanField(default=True)


class Settings_currenttextpage(Settings):
    pass


class Settings_currenttextquery(Settings):
    pass


class Settings_currenttextsort(Settings):
    pass


class Settings_currentwordpage(Settings):
    pass


class Settings_currentwordquery(Settings):
    pass


class Settings_currentwordstatus(Settings):
    pass


class Settings_currentwordsort(Settings):
    pass

''' used in text_list to filter the texts (and terms) to display'''
class Settings_currentfilter_lang(Settings):
    language = models.OneToOneField(Languages, related_name='filterlangforthislanguage',
                                     on_delete=models.CASCADE)
    is_strong = models.BooleanField(default=True)


''' used in text_list to filter the texts to display'''
class Settings_currentfilter_texttag(Settings):
    texttag = models.OneToOneField(Texttags, related_name='filtertagforthistexttag',
                                    on_delete=models.CASCADE)
    is_strong = models.BooleanField(default=True)


''' used in text_list to filter the terms to display'''
class Settings_currentfilter_text(Settings):
    text = models.OneToOneField(Texts, related_name='filtertextforthistext',
                                 on_delete=models.CASCADE)
    is_strong = models.BooleanField(default=True)


''' used in text_list to filter the terms to display'''
class Settings_currentfilter_word(Settings):
    word = models.OneToOneField(Words, related_name='filterwordforthisword',
                                 on_delete=models.CASCADE)
    is_strong = models.BooleanField(default=True)


''' used when clicking on check/uncheck all in term_list (or export2anki or selectivebackup)
    it stores all the words which are in table (in all the pages)'''
class Settings_selected_rows(Settings):
    possible_selected_rows = models.TextField()

''' used when clicking on check/uncheck all in term_list (or export2anki or selectivebackup)
    it stores the current number of selected rows (in all the pages)'''
class Settings_selected_rows_nb(Settings):
    currently_selected_rows_nb = models.IntegerField(default=0)

#####################################################
#             end 'settings':                       #
#####################################################
''' load and get the real name and the ISO language codes for the Fixtures of languages 
    (in lwt.constants.py) for the learning language for the Language User wants to learn
                            and for the "origin" language (language User knows)
    we used this to modify the dict1uri and dict2uri with the correct language destination
      Called : - when displaying the admin languages when creating the form for the User
              - when importing LWT demo

    Ex: http://www.wordreference.com/fr••/###
           becomes ==> http://www.wordreference.com/fren/###
    '''
def substitute_in_dictURI(user, code_learninglang_OR_obj, called_by_Obj=False):
    import re
#     import json
    # for the origin lang too (language I know):
    origin_lang_code = user.origin_lang_code
    for lang in LANGUAGES_CODE:
        if lang['1'] ==  origin_lang_code:
            origin_lang = lang
            break
    
    # for the chosen lang (language I want to learn)
    # the ADMIN has the basic languages (owner=1)
    if not called_by_Obj:
        learning_lang = Languages.objects.filter(owner=1, code_639_1=code_learninglang_OR_obj).values()[0]
        googletranslate_dicturi = learning_lang['googletranslateuri']
    else:
        learning_lang = code_learninglang_OR_obj
        googletranslate_dicturi = learning_lang.googletranslateuri

    def _set_attr_OR_key(obj, el, val):
        if not called_by_Obj:
            obj[el] = val
            return obj
        else:
            setattr(obj, el, val)
            return obj
    def _get_attr_OR_key(obj, el):
        if not called_by_Obj:
            return obj[el]
        else:
            return getattr(obj, el)

    # then change the placeholder string for the translation:
    # there are several links in dicturi, so each of the 'ifs' can be called also
    if '<LCNAME>' in _get_attr_OR_key(learning_lang, "dicturi"):
        learning_lang = _set_attr_OR_key(learning_lang, "dicturi", 
                    re.sub(r'<LCNAME>', origin_lang['name'].lower(), _get_attr_OR_key(learning_lang, "dicturi")))
    if '<NAME>' in _get_attr_OR_key(learning_lang, "dicturi"):
        learning_lang = _set_attr_OR_key(learning_lang, "dicturi", 
                    re.sub(r'<NAME', origin_lang['name'], _get_attr_OR_key(learning_lang, "dicturi")))
    if '<2TCODE>' in _get_attr_OR_key(learning_lang, "dicturi"):
        learning_lang = _set_attr_OR_key(learning_lang, "dicturi", 
                    re.sub(r'<2TCODE>', origin_lang['2T'], _get_attr_OR_key(learning_lang, "dicturi")))
    if '<1CODE' in _get_attr_OR_key(learning_lang, "dicturi"):
        learning_lang = _set_attr_OR_key(learning_lang, "dicturi", 
                    re.sub(r'<1CODE>', origin_lang['1'], _get_attr_OR_key(learning_lang, "dicturi")))
    # always true:
    learning_lang = _set_attr_OR_key(learning_lang, "googletranslateuri", 
                        re.sub(r'<1CODE>', origin_lang['1'], googletranslate_dicturi))

    return learning_lang        

""" This is called when saving user via allauth registration.
    We override this to set additional data on user object. """
class UserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        # Do not persist the user yet so we pass commit=False  (last argument)
        user = super(UserAccountAdapter, self).save_user(request, user, form, commit=commit)
        user.origin_lang_code = form.cleaned_data.get('origin_lang_code')
        user.save()

        # create a duplicate of the Admin's language that the User has chosen
        # the Admin 'lingl` owns the basis of the languages
        AdminUser_learning_lang_id = form.cleaned_data['AdminUser_learning_lang_id']  
        learning_lang = Languages.objects.get(id=int(AdminUser_learning_lang_id))
        learning_lang.pk = None
        learning_lang.owner = user
        # set dict1uri and dict2uri 
        learning_lang = substitute_in_dictURI(user, learning_lang, called_by_Obj=True)
        dicturi = learning_lang.dicturi.split(',')
        learning_lang.dict1uri = dicturi[0].strip()
        learning_lang.dict2uri = dicturi[1].strip()
        learning_lang.save()
        # and set this as the currentlang in database (can't put in cookie for the moment because no 'request')
        Settings_currentlang_id.objects.create(owner=user, stvalue=learning_lang.id)
        Settings_currentlang_name.objects.create(owner=user, stvalue=learning_lang.name)
        return user    


''' Used insided Backup & Restore to upload a backup file '''
class Restore(models.Model):
    owner = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE) # each user has his own set of the database
    restore_file_name = models.CharField(max_length=255, blank=True) # IS it useful?
    restore_file = models.FileField(blank=True)
    import_oldlwt = models.FileField(blank=True)
#     restore_oldlwt_file = models.FileField()


''' to upload a text file. in text_detail.html '''
class Uploaded_text(models.Model):
    owner = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE) # each user has his own set of the database
    uploaded_text = models.FileField(blank=True)
