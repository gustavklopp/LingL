from django.utils.translation import ugettext as _


STATUS_CHOICES = { 0: {'nb':0, 'name': _('Unknown'), 'abbr':_('Unk.'), 'small': '[0]'},
                   1: {'nb':1, 'name': _('Learning'), 'abbr': ('Lear.'), 'small': '[1-99]'},
                   100: {'nb':100, 'name': _('Well known'), 'abbr':_('Wkn.'), 'small': '[100]'},
                   101: {'nb':101, 'name': _('Ignored'), 'abbr':_('Ign.'), 'small': '[101]'}
                }

# Number of words where an alert is trigger to archive or delete some texts
MAX_WORDS_NOTICE = 2000
MAX_WORDS_WARNING = 3000
MAX_WORDS_DANGER = 4000

'''
(with the addition of Obtained from github user 
@Anurbol: https://github.com/anurbol/languages-iso-639-1-2-3-json/blob/master/data.js 
it doesn't contain everything since some languages are not found in Django:
i.e doing get_language_info(LANGUAGES_CODE['1']) gets nothing so I remove this language.
In addition, I've modified Chinese since Django_code is different from the LANGUAGES_CODE['1']
(because of the distinction between 'zh-hans' and 'zh-hant')
'''
LANGUAGES_CODE = [
 {'django_code':'zh-hans', '1':'zh',  '2':'zho',  '2T':'zho', '2B':'chi', '3':'zho', 'local':'中文', 'name':'Chinese'},
 {'django_code':'zh-hant', '1':'zh',  '2':'zho',  '2T':'zho', '2B':'chi', '3':'zho', 'local':'中文', 'name':'Chinese'},
 {'django_code':'af', '1':'af', '2':'afr', '2B':'afr', '2T':'afr', '3':'afr', 'local':'Afrikaans', 'name':'Afrikaans'},
 {'django_code':'sq', '1':'sq', '2':'sqi', '2B':'alb', '2T':'sqi', '3':'sqi', 'local':'Shqip', 'name':'Albanian'},
 {'django_code':'ar', '1':'ar', '2':'ara', '2B':'ara', '2T':'ara', '3':'ara', 'local':'العربية', 'name':'Arabic'},
 {'django_code':'hy', '1':'hy', '2':'hye', '2B':'arm', '2T':'hye', '3':'hye', 'local':'Հայերեն', 'name':'Armenian'},
 {'django_code':'az', '1':'az', '2':'aze', '2B':'aze', '2T':'aze', '3':'aze', 'local':'Azərbaycanca', 'name':'Azerbaijani'},
 {'django_code':'eu', '1':'eu', '2':'eus', '2B':'baq', '2T':'eus', '3':'eus', 'local':'Euskara', 'name':'Basque'},
 {'django_code':'be', '1':'be', '2':'bel', '2B':'bel', '2T':'bel', '3':'bel', 'local':'Беларуская', 'name':'Belarusian'},
 {'django_code':'bn', '1':'bn', '2':'ben', '2B':'ben', '2T':'ben', '3':'ben', 'local':'বাংলা', 'name':'Bengali'},
 {'django_code':'bs', '1':'bs', '2':'bos', '2B':'bos', '2T':'bos', '3':'bos', 'local':'Bosanski', 'name':'Bosnian'},
 {'django_code':'br', '1':'br', '2':'bre', '2B':'bre', '2T':'bre', '3':'bre', 'local':'Brezhoneg', 'name':'Breton'},
 {'django_code':'bg', '1':'bg', '2':'bul', '2B':'bul', '2T':'bul', '3':'bul', 'local':'Български', 'name':'Bulgarian'},
 {'django_code':'my', '1':'my', '2':'mya', '2B':'bur', '2T':'mya', '3':'mya', 'local':'မြန်မာဘာသာ', 'name':'Burmese'},
 {'django_code':'ca', '1':'ca', '2':'cat', '2B':'cat', '2T':'cat', '3':'cat', 'local':'Català', 'name':'Catalan'},
 {'django_code':'hr', '1':'hr', '2':'hrv', '2B':'hrv', '2T':'hrv', '3':'hrv', 'local':'Hrvatski', 'name':'Croatian'},
 {'django_code':'cs', '1':'cs', '2':'ces', '2B':'cze', '2T':'ces', '3':'ces', 'local':'Čeština', 'name':'Czech'},
 {'django_code':'da', '1':'da', '2':'dan', '2B':'dan', '2T':'dan', '3':'dan', 'local':'Dansk', 'name':'Danish'},
 {'django_code':'nl', '1':'nl', '2':'nld', '2B':'dut', '2T':'nld', '3':'nld', 'local':'Nederlands', 'name':'Dutch'},
 {'django_code':'en', '1':'en', '2':'eng', '2B':'eng', '2T':'eng', '3':'eng', 'local':'English', 'name':'English'},
 {'django_code':'eo', '1':'eo', '2':'epo', '2B':'epo', '2T':'epo', '3':'epo', 'local':'Esperanto', 'name':'Esperanto'},
 {'django_code':'et', '1':'et', '2':'est', '2B':'est', '2T':'est', '3':'est', 'local':'Eesti', 'name':'Estonian'},
 {'django_code':'fi', '1':'fi', '2':'fin', '2B':'fin', '2T':'fin', '3':'fin', 'local':'Suomi', 'name':'Finnish'},
 {'django_code':'fr', '1':'fr', '2':'fra', '2B':'fre', '2T':'fra', '3':'fra', 'local':'Français', 'name':'French'},
 {'django_code':'gl', '1':'gl', '2':'glg', '2B':'glg', '2T':'glg', '3':'glg', 'local':'Galego', 'name':'Galician'},
 {'django_code':'ka', '1':'ka', '2':'kat', '2B':'geo', '2T':'kat', '3':'kat', 'local':'ქართული', 'name':'Georgian'},
 {'django_code':'de', '1':'de', '2':'deu', '2B':'ger', '2T':'deu', '3':'deu', 'local':'Deutsch', 'name':'German'},
 {'django_code':'el', '1':'el', '2':'ell', '2B':'gre', '2T':'ell', '3':'ell', 'local':'Ελληνικά', 'name':'Greek'},
 {'django_code':'he', '1':'he', '2':'heb', '2B':'heb', '2T':'heb', '3':'heb', 'local':'עברית', 'name':'Hebrew'},
 {'django_code':'hi', '1':'hi', '2':'hin', '2B':'hin', '2T':'hin', '3':'hin', 'local':'हिन्दी', 'name':'Hindi'},
 {'django_code':'hu', '1':'hu', '2':'hun', '2B':'hun', '2T':'hun', '3':'hun', 'local':'Magyar', 'name':'Hungarian'},
 {'django_code':'ia', '1':'ia', '2':'ina', '2B':'ina', '2T':'ina', '3':'ina', 'local':'Interlingua', 'name':'Interlingua'},
 {'django_code':'id', '1':'id', '2':'ind', '2B':'ind', '2T':'ind', '3':'ind', 'local':'Bahasa Indonesia', 'name':'Indonesian'},
 {'django_code':'ga', '1':'ga', '2':'gle', '2B':'gle', '2T':'gle', '3':'gle', 'local':'Gaeilge', 'name':'Irish'},
 {'django_code':'ig', '1':'ig', '2':'ibo', '2B':'ibo', '2T':'ibo', '3':'ibo', 'local':'Igbo', 'name':'Igbo'},
 {'django_code':'io', '1':'io', '2':'ido', '2B':'ido', '2T':'ido', '3':'ido', 'local':'Ido', 'name':'Ido'},
 {'django_code':'is', '1':'is', '2':'isl', '2B':'ice', '2T':'isl', '3':'isl', 'local':'Íslenska', 'name':'Icelandic'},
 {'django_code':'it', '1':'it', '2':'ita', '2B':'ita', '2T':'ita', '3':'ita', 'local':'Italiano', 'name':'Italian'},
 {'django_code':'ja', '1':'ja', '2':'jpn', '2B':'jpn', '2T':'jpn', '3':'jpn', 'local':'日本語', 'name':'Japanese'},
 {'django_code':'kn', '1':'kn', '2':'kan', '2B':'kan', '2T':'kan', '3':'kan', 'local':'ಕನ್ನಡ', 'name':'Kannada'},
 {'django_code':'kk', '1':'kk', '2':'kaz', '2B':'kaz', '2T':'kaz', '3':'kaz', 'local':'Қазақша', 'name':'Kazakh'},
 {'django_code':'km', '1':'km', '2':'khm', '2B':'khm', '2T':'khm', '3':'khm', 'local':'ភាសាខ្មែរ', 'name':'Khmer'},
 {'django_code':'ky', '1':'ky', '2':'kir', '2B':'kir', '2T':'kir', '3':'kir', 'local':'Кыргызча', 'name':'Kyrgyz'},
 {'django_code':'ko', '1':'ko', '2':'kor', '2B':'kor', '2T':'kor', '3':'kor', 'local':'한국어', 'name':'Korean'},
 {'django_code':'lb', '1':'lb', '2':'ltz', '2B':'ltz', '2T':'ltz', '3':'ltz', 'local':'Lëtzebuergesch', 'name':'Luxembourgish'},
 {'django_code':'lt', '1':'lt', '2':'lit', '2B':'lit', '2T':'lit', '3':'lit', 'local':'Lietuvių', 'name':'Lithuanian'},
 {'django_code':'lv', '1':'lv', '2':'lav', '2B':'lav', '2T':'lav', '3':'lav', 'local':'Latviešu', 'name':'Latvian'},
 {'django_code':'mk', '1':'mk', '2':'mkd', '2B':'mac', '2T':'mkd', '3':'mkd', 'local':'Македонски', 'name':'Macedonian'},
 {'django_code':'ml', '1':'ml', '2':'mal', '2B':'mal', '2T':'mal', '3':'mal', 'local':'മലയാളം', 'name':'Malayalam'},
 {'django_code':'mr', '1':'mr', '2':'mar', '2B':'mar', '2T':'mar', '3':'mar', 'local':'मराठी', 'name':'Marathi'},
 {'django_code':'mn', '1':'mn', '2':'mon', '2B':'mon', '2T':'mon', '3':'mon', 'local':'Монгол', 'name':'Mongolian'},
 {'django_code':'ne', '1':'ne', '2':'nep', '2B':'nep', '2T':'nep', '3':'nep', 'local':'नेपाली', 'name':'Nepali'},
 {'django_code':'nb', '1':'nb', '2':'nob', '2B':'nob', '2T':'nob', '3':'nob', 'local':'Norsk (Bokmål)', 'name':'Norwegian Bokmål'},
 {'django_code':'nn', '1':'nn', '2':'nno', '2B':'nno', '2T':'nno', '3':'nno', 'local':'Norsk (Nynorsk)', 'name':'Norwegian Nynorsk'},
 {'django_code':'os', '1':'os', '2':'oss', '2B':'oss', '2T':'oss', '3':'oss', 'local':'Ирон æвзаг', 'name':'Ossetian'},
 {'django_code':'pa', '1':'pa', '2':'pan', '2B':'pan', '2T':'pan', '3':'pan', 'local':'ਪੰਜਾਬੀ', 'name':'Panjabi'},
 {'django_code':'fa', '1':'fa', '2':'fas', '2B':'per', '2T':'fas', '3':'fas', 'local':'فارسی', 'name':'Persian'},
 {'django_code':'pl', '1':'pl', '2':'pol', '2B':'pol', '2T':'pol', '3':'pol', 'local':'Polski', 'name':'Polish'},
 {'django_code':'pt', '1':'pt', '2':'por', '2B':'por', '2T':'por', '3':'por', 'local':'Português', 'name':'Portuguese'},
 {'django_code':'ro', '1':'ro', '2':'ron', '2B':'rum', '2T':'ron', '3':'ron', 'local':'Română', 'name':'Romanian'},
 {'django_code':'ru', '1':'ru', '2':'rus', '2B':'rus', '2T':'rus', '3':'rus', 'local':'Русский', 'name':'Russian'},
 {'django_code':'sr', '1':'sr', '2':'srp', '2B':'srp', '2T':'srp', '3':'srp', 'local':'Српски', 'name':'Serbian'},
 {'django_code':'gd', '1':'gd', '2':'gla', '2B':'gla', '2T':'gla', '3':'gla', 'local':'Gàidhlig', 'name':'Gaelic'},
 {'django_code':'sk', '1':'sk', '2':'slk', '2B':'slo', '2T':'slk', '3':'slk', 'local':'Slovenčina', 'name':'Slovak'},
 {'django_code':'sl', '1':'sl', '2':'slv', '2B':'slv', '2T':'slv', '3':'slv', 'local':'Slovenščina', 'name':'Slovene'},
 {'django_code':'es', '1':'es', '2':'spa', '2B':'spa', '2T':'spa', '3':'spa', 'local':'Español', 'name':'Spanish'},
 {'django_code':'sw', '1':'sw', '2':'swa', '2B':'swa', '2T':'swa', '3':'swa', 'local':'Kiswahili', 'name':'Swahili'},
 {'django_code':'sv', '1':'sv', '2':'swe', '2B':'swe', '2T':'swe', '3':'swe', 'local':'Svenska', 'name':'Swedish'},
 {'django_code':'ta', '1':'ta', '2':'tam', '2B':'tam', '2T':'tam', '3':'tam', 'local':'தமிழ்', 'name':'Tamil'},
 {'django_code':'te', '1':'te', '2':'tel', '2B':'tel', '2T':'tel', '3':'tel', 'local':'తెలుగు', 'name':'Telugu'},
 {'django_code':'tg', '1':'tg', '2':'tgk', '2B':'tgk', '2T':'tgk', '3':'tgk', 'local':'Тоҷикӣ', 'name':'Tajik'},
 {'django_code':'th', '1':'th', '2':'tha', '2B':'tha', '2T':'tha', '3':'tha', 'local':'ภาษาไทย', 'name':'Thai'},
 {'django_code':'tk', '1':'tk', '2':'tuk', '2B':'tuk', '2T':'tuk', '3':'tuk', 'local':'Türkmençe', 'name':'Turkmen'},
 {'django_code':'tr', '1':'tr', '2':'tur', '2B':'tur', '2T':'tur', '3':'tur', 'local':'Türkçe', 'name':'Turkish'},
 {'django_code':'tt', '1':'tt', '2':'tat', '2B':'tat', '2T':'tat', '3':'tat', 'local':'Татарча', 'name':'Tatar'},
 {'django_code':'uk', '1':'uk', '2':'ukr', '2B':'ukr', '2T':'ukr', '3':'ukr', 'local':'Українська', 'name':'Ukrainian'},
 {'django_code':'ur', '1':'ur', '2':'urd', '2B':'urd', '2T':'urd', '3':'urd', 'local':'اردو', 'name':'Urdu'},
 {'django_code':'uz', '1':'uz', '2':'uzb', '2B':'uzb', '2T':'uzb', '3':'uzb', 'local':'O‘zbek', 'name':'Uzbek'},
 {'django_code':'vi', '1':'vi', '2':'vie', '2B':'vie', '2T':'vie', '3':'vie', 'local':'Tiếng Việt', 'name':'Vietnamese'},
 {'django_code':'cy', '1':'cy', '2':'cym', '2B':'wel', '2T':'cym', '3':'cym', 'local':'Cymraeg', 'name':'Welsh'},
 {'django_code':'fy', '1':'fy', '2':'fry', '2B':'fry', '2T':'fry', '3':'fry', 'local':'Frysk', 'name':'Western Frisian'}
 ]
