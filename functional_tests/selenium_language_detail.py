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
from lwt.factories import *
from lwt.views._utilities_views import *
from selenium.webdriver.common import desired_capabilities
from .selenium_base import BasePage

class Language_detail(BasePage_loggedin):

    def test_using_predefined_language(self):
        response = self.selenium.get('{}/language_detail?new=0'.format(self.live_server_url))
        self.find(By.CLASS_NAME, 'input-group-addon').click()
        self.find(By.LINK_TEXT, 'Slovenian').click()
        self.find(By.ID, 'submit-id-save').click()
        self.assertEqual(self.selenium.current_url, '{}/language_list/'.format(self.live_server_url))

    def test_creating_same_name_languages(self):
        # define a language
        language_1 = LanguagesFactory(owner=self.user_1)
        # first language with the same name
        self.selenium.get('{}/language_detail?new=0'.format(self.live_server_url))
        self.find(By.ID, 'id_name').send_keys(language_1.name)
        self.find(By.ID, 'id_dict1uri').send_keys(language_1.dict1uri)
        self.find(By.ID, 'id_googletranslateuri').send_keys(language_1.googletranslateuri)
        self.find(By.ID, 'id_exporttemplate').send_keys(language_1.exporttemplate)
        self.find(By.ID, 'id_charactersubstitutions').send_keys(language_1.charactersubstitutions)
        self.find(By.ID, 'id_regexpsplitsentences').send_keys(language_1.regexpsplitsentences)
        self.find(By.ID, 'id_exceptionssplitsentences').send_keys(language_1.exceptionssplitsentences)
        self.find(By.ID, 'id_regexpwordcharacters').send_keys(language_1.regexpwordcharacters)
#         self.find(By.ID, 'id_code_639_1').send_keys(language_1.code_639_1)
#         self.find(By.ID, 'id_code_639_2t').send_keys(language_1.code_639_2t)
#         self.find(By.ID, 'id_code_639_2b').send_keys(language_1.code_639_2b)
#         self.find(By.ID, 'id_django_code').send_keys(language_1.django_code)
        self.find(By.ID, 'submit-id-save').click()
        self.assertEqual(self.selenium.current_url, '{}/language_detail/?new=0'.format(self.live_server_url))
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