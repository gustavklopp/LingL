# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
# use to create session cookies
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings 
from django.contrib.auth import ( SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY, get_user_model)
# second party
import time
import random
import os

from selenium import webdriver # used for firefoxProfile()
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#third party

# local
from functional_tests.factories import *
from lwt.models import MyUser
from lwt.views._utilities_views import *
from selenium.webdriver.common import desired_capabilities
from .selenium_base import Base


class Language_detail(Base):
    
    def setUp(self):
        super(Language_detail, self).setUp()

        self.pwd = 'selenium12345!!!'
        self.admin = UserFactory(username='admin', id=1, password=self.pwd)
        self.adminLanguage1 = LanguagesFactory(name='adminLanguage1',code_639_1='en' , django_code='en', owner=self.admin)
        self.adminLanguage2 = LanguagesFactory(name='adminLanguage2',code_639_1='fr' , django_code='fr', owner=self.admin)
        self.adminLanguage3 = LanguagesFactory(name='adminLanguage3',code_639_1='it' , django_code='it', owner=self.admin)
        self.adminLanguage4 = LanguagesFactory(name='adminLanguage4',code_639_1='sl' , django_code='sl', owner=self.admin)
        self.adminLanguage5 = LanguagesFactory(name='adminLanguage5',code_639_1='de' , django_code='de', owner=self.admin)
        self.adminLanguage6 = LanguagesFactory(name='adminLanguage6',code_639_1='pt' , django_code='pt', owner=self.admin)
        self.adminLanguage7 = LanguagesFactory(name='adminLanguage7',code_639_1='he' , django_code='he', owner=self.admin)
        self.adminLanguage8 = LanguagesFactory(name='adminLanguage8',code_639_1='th' , django_code='th', owner=self.admin)
        self.adminLanguage9 = LanguagesFactory(name='adminLanguage9',code_639_1='ko' , django_code='ko', owner=self.admin)
        self.adminLanguage10 = LanguagesFactory(name='adminLanguage10',code_639_1='ja' , django_code='ja', owner=self.admin)
        self.adminLanguage11 = LanguagesFactory(name='adminLanguage11',code_639_1='zh-cn', django_code='zh-cn', owner=self.admin)
        
        self.pwd = 'selenium12345!!!'
        self.user_1 = UserFactory(password=self.pwd, origin_lang_code='en')
        self.selenium = WebDriver()
        self.language_1 = EnglishLanguagesFactory(owner=self.user_1)
        Settings_currentlang_idFactory(owner=self.user_1, stvalue=self.language_1.id)
        self.selenium.get('{}'.format(self.live_server_url))
        self.find(By.NAME, 'login').send_keys(self.user_1.username)
        self.find(By.NAME, 'password').send_keys(self.pwd)
        self.find(By.CSS_SELECTOR, "button[type='submit']").click()

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super(Text_read, cls).tearDownClass()

    def tearDown(self):
        self.selenium.quit()
        super(Language_detail, self).tearDown()

    def test_using_predefined_language(self):
        self.selenium.get('{}/language_list/'.format(self.live_server_url))
        self.find(By.XPATH, '//a[@role="button"  and contains(text(), "New Language")]').click()
#         self.selenium.get('{}/language_detail?new=0'.format(self.live_server_url))
        self.find(By.CLASS_NAME, 'input-group-append').click()
        self.find(By.LINK_TEXT, 'Slovenian').click()
#         self.wait_until_text_appear((By.CSS_SELECTOR,'input#id_dict1uri'), 'https://glosbe.com/gapi/translate?from=eng&&dest=•••&&format=json')
        self.find(By.ID, 'submit-id-save').click()
        self.assertEqual(self.selenium.current_url, '{}/language_list/'.format(self.live_server_url))
        langs = self.finds(By.CSS_SELECTOR, '#lang_table tbody tr')
        self.assertEqual(len(langs), 2)
        row_current_lang = None
        idx = None
        for idx, lang in enumerate(langs):
            try:
                row_current_lang = lang.find_element_by_css_selector('img[alt="Current Language"]')
                idx = idx
            except:
                continue
        lang_tds = langs[idx].find_elements_by_css_selector('td')
        self.assertTrue(lang_tds[3], 'Slovenian')
        
    def test_editing_a_language(self):
        self.selenium.get('{}/language_list/'.format(self.live_server_url))
        self.find(By.XPATH, '//a[@role="button"  and contains(text(), "New Language")]').click()
#         self.selenium.get('{}/language_detail?new=0'.format(self.live_server_url))
        self.find(By.CLASS_NAME, 'input-group-append').click()
        self.find(By.LINK_TEXT, 'Slovenian').click()
        self.find(By.ID, 'submit-id-save').click()
        self.assertEqual(self.selenium.current_url, '{}/language_list/'.format(self.live_server_url))
        langs = self.finds(By.CSS_SELECTOR, '#lang_table tbody tr')
        self.assertEqual(len(langs), 2)
        for idx, lang in enumerate(langs):
            lang_tds = lang.find_elements_by_css_selector('td')
            if lang_tds[3].text == 'English':
                id = langs[idx].get_attribute('data-val')
                langs[idx].find_element_by_css_selector('img[alt="Edit"]').click()
                break
        self.assertEqual(self.selenium.current_url, '{}/language_detail/?edit={}'.format(self.live_server_url, id))
        # change name
        name = self.find(By.ID, 'id_name')
        name.clear()
        name.send_keys('NEWLANGUAGE')
        dict1uri = self.find(By.ID, 'id_dict1uri')
        dict1uri.clear()
        dict1uri.send_keys('NEWDICT1URI')
        self.find(By.ID, 'submit-id-save').click()
        self.wait_until_appear(By.ID, 'lang_table')
        self.assertEqual(self.selenium.current_url, '{}/language_list/'.format(self.live_server_url))
        langs = self.finds(By.CSS_SELECTOR, '#lang_table tbody tr')
        self.assertEqual(len(langs), 2)
        for idx, lang in enumerate(langs):
            lang_tds = lang.find_elements_by_css_selector('td')
            if lang_tds[3].text == 'NEWLANGUAGE':
                self.assertEqual(lang_tds[6].text, 'NEWDICT1URI')
                break

#     def test_creating_same_name_languages(self):
#         # define a language
#         language_1 = LanguagesFactory(owner=self.user_1)
#         # first language with the same name
#         self.selenium.get('{}/language_detail?new=0'.format(self.live_server_url))
#         self.find(By.ID, 'id_name').send_keys(language_1.name)
#         self.find(By.ID, 'id_dict1uri').send_keys(language_1.dict1uri)
#         self.find(By.ID, 'id_googletranslateuri').send_keys(language_1.googletranslateuri)
#         self.find(By.ID, 'id_exporttemplate').send_keys(language_1.exporttemplate)
#         self.find(By.ID, 'id_charactersubstitutions').send_keys(language_1.charactersubstitutions)
#         self.find(By.ID, 'id_regexpsplitsentences').send_keys(language_1.regexpsplitsentences)
#         self.find(By.ID, 'id_exceptionssplitsentences').send_keys(language_1.exceptionssplitsentences)
#         self.find(By.ID, 'id_regexpwordcharacters').send_keys(language_1.regexpwordcharacters)
# #         self.find(By.ID, 'id_code_639_1').send_keys(language_1.code_639_1)
# #         self.find(By.ID, 'id_code_639_2t').send_keys(language_1.code_639_2t)
# #         self.find(By.ID, 'id_code_639_2b').send_keys(language_1.code_639_2b)
# #         self.find(By.ID, 'id_, django_code').send_keys(language_1.django_code)
#         self.find(By.ID, 'submit-id-save').click()
#         self.assertEqual(self.selenium.current_url, '{}/language_detail/?new=0'.format(self.live_server_url))
#         self.selenium.get('{}'.format(self.live_server_url))
#         # second language with the diferent name
#         language_2 = LanguagesFactory(owner=self.user_1)
#         self.selenium.get('{}/language_detail?new=0'.format(self.live_server_url))
#         self.find(By.ID, 'id_name').send_keys('NEWLANG')
#         self.find(By.ID, 'id_dict1uri').send_keys(language_2.dict1uri)
#         self.find(By.ID, 'id_googletranslateuri').send_keys(language_2.googletranslateuri)
#         self.find(By.ID, 'id_exporttemplate').send_keys(language_2.exporttemplate)
#         self.find(By.ID, 'id_charactersubstitutions').send_keys(language_2.charactersubstitutions)
#         self.find(By.ID, 'id_regexpsplitsentences').send_keys(language_2.regexpsplitsentences)
#         self.find(By.ID, 'id_exceptionssplitsentences').send_keys(language_2.exceptionssplitsentences)
#         self.find(By.ID, 'id_regexpwordcharacters').send_keys(language_2.regexpwordcharacters)
#         self.find(By.ID, 'submit-id-save').click()
#         self.assertEqual(self.selenium.current_url, '{}/language_list/'.format(self.live_server_url))