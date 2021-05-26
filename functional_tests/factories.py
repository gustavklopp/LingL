from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# third-party
import factory
import factory.fuzzy
# local
from lwt.models import *
from functional_tests.corpus_text import *
from django.templatetags.i18n import language


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MyUser
    
    username = factory.Faker('first_name')
    password = factory.PostGenerationMethodCall('set_password', '12345')
    origin_lang_code = factory.fuzzy.FuzzyText(length=2)


class LanguagesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Languages
    
    owner = factory.SubFactory(UserFactory)
    name = factory.fuzzy.FuzzyText()
    dict1uri = 'LINKDICT1URI'
#     dict1uri = "https://glosbe.com/gapi/translate?from=eng&&dest=fra&&format=json"
#     # for ex: English => French   default="https://glosbe.com/gapi/translate?from=eng&dest=fra&format=json")  
#     dict2uri = "https://en.wiktionary.org/wiki/###"
#     googletranslateuri = "*http://translate.google.com/?ie=UTF-8&sl=en&tl=fr&text=###"
    
class GermanLanguagesFactory(LanguagesFactory):
    ''' using glosbe.api '''
    class Meta:
        model = Languages
    
    name = 'German'
    dict1uri = 'https://glosbe.com/gapi/translate?from=deu&&dest=eng&&format=json'
#     # for ex: English => French   default="https://glosbe.com/gapi/translate?from=eng&dest=fra&format=json")  
    dict2uri = "https://en.wiktionary.org/wiki/###"
    googletranslateuri = "*http://translate.google.com/?ie=UTF-8&sl=de&tl=en&text=###"

    
class EnglishLanguagesFactory(LanguagesFactory):
    ''' using wordreference website '''
    class Meta:
        model = Languages
    
    name = 'English'
    dict1uri = "http://www.wordreference.com/enfr/###"
#     # for ex: English => French   default="https://glosbe.com/gapi/translate?from=eng&dest=fra&format=json")  
    dict2uri = "https://en.wiktionary.org/wiki/###"
    googletranslateuri = "*http://translate.google.com/?ie=UTF-8&sl=en&tl=fr&text=###"
    
    
class ChineseLanguagesFactory(LanguagesFactory):
    class Meta:
        model = Languages
    name = 'Chinese' 
    dict1uri = 'http://ce.linedict.com/#/cnen/search?query=###'
    dict2uri = 'https://kanji.koohii.com/study/kanji/###' 
    googletranslateuri = '*http://translate.google.com/?ie=UTF-8&sl=••&tl=••&text=###'
    exporttemplate = '$y\\t$t\\n'
    textsize = '150'
    charactersubstitutions = '´=\'|`=\'|’=\'|‘=\'|...=…|..=‥'
    regexpsplitsentences = '.!?:;。！？：；'
    exceptionssplitsentences = 'Mr.|Dr.|[A-Z].|Vd.|Vds.'
    regexpwordcharacters = '一-龥'
    removespaces = 1
    spliteachchar = 1
    righttoleft = 0


class HebrewLanguagesFactory(LanguagesFactory):
    class Meta:
        model = Languages
    name = 'Hebrew' 
    dict1uri = 'https://glosbe.com/gapi/translate?from=heb&&dest=eng&&format=json'
    dict2uri = 'http://morfix.mako.co.il/default.aspx?q=###' 
    googletranslateuri = '*http://translate.google.com/?ie=UTF-8&sl=iw&tl=en&text=###'
    exporttemplate = '$y\\t$t\\n'
    textsize = '150'
    charactersubstitutions = ''
    regexpsplitsentences = '.!?:;'
    exceptionssplitsentences = ''
#     regexpwordcharacters = '\\x{0590}-\\x{05FF}'# NOT WORKING
    regexpwordcharacters = '\u0590-\u05FF'
    removespaces = 0
    spliteachchar = 0
    righttoleft = 1
 
 
class TextsFactory(factory.django.DjangoModelFactory):
    ''' Create random text '''
    class Meta:
        model = Texts
    
    owner = factory.SubFactory(UserFactory)
    language = factory.SubFactory(LanguagesFactory)
    title = factory.fuzzy.FuzzyText()
    text =  factory.Faker('text')

    
class GermanTextsFactory(TextsFactory):
    ''' Creating non random true text thanks to 'corpus_text' module '''
    class Meta:
        model = Texts

#     corpus_text = Corpus_text('German', 1)
    title, text = corpus_text('German', nb_of_lines=1)


class EnglishTextsFactory(TextsFactory):
    ''' Creating non random true text thanks to 'corpus_text' module '''
    class Meta:
        model = Texts

#     corpus_text = Corpus_text('German', 1)
    title, text = corpus_text('English', nb_of_lines=5)


class SettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Settings

    owner = factory.SubFactory(UserFactory)
    stvalue = factory.fuzzy.FuzzyText(length=3, chars=[str(x) for x in range(10)])
    stdft = "" # default value
    isinteger = False
#     min = models.IntegerField( null=True) # min value allowed for the user
#     max = models.IntegerField(null=True) # max value allowed for the user
#     isinteger = models.BooleanField(default='False')

class Settings_currentlang_idFactory(SettingsFactory):
    class Meta:
        model = Settings_currentlang_id

    isinteger = True
