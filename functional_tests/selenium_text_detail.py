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

class Text_detail(Base):

    def setUp(self):
        super(Text_detail, self).setUp()
        self.pwd = 'selenium12345!!!'
        self.user_1 = UserFactory(password=self.pwd)
        self.selenium = WebDriver()
        self.language_1 = EnglishLanguagesFactory(owner=self.user_1)
        Settings_currentlang_idFactory(owner=self.user_1, stvalue=self.language_1.id)
        self.selenium.get('{}'.format(self.live_server_url))
        self.find(By.NAME, 'login').send_keys(self.user_1.username)
        self.find(By.NAME, 'password').send_keys(self.pwd)
        self.find(By.CSS_SELECTOR, "button[type='submit']").click()

    def tearDown(self):
        self.selenium.quit()
        super(Text_detail, self).tearDown()

    def test_create_a_new_text(self):  
        language_1 = LanguagesFactory(owner=self.user_1)
        self.selenium.get('{}/text_detail/?new=0/'.format(self.live_server_url))
        select = Select(self.find(By.NAME,'language'))
        select.select_by_visible_text(self.language_1.name)
        title_str = 'an Example of title'
        title = self.find(By.NAME, 'title')
        title.send_keys(title_str)
        text = self.find(By.NAME,'text')
        text.send_keys('This is the content of this text.')
        save = self.find(By.ID, 'submit-id-save')
        save.click()
#         time.sleep(5)
#         self.selenium.implicitly_wait(10)
#         self.wait_until(By.ID, 'text_table')
        self.selenium.get('{}/text_list/'.format(self.live_server_url))
        self.assertEqual(self.selenium.current_url, '{}/text_list/'.format(self.live_server_url))
        self.find(By.CSS_SELECTOR, '#filterlangform input[value="2"]').click()
        self.wait_until_disappear(By.XPATH, '//td[contains(text(), "No matching records found")]')
        self.wait_until_appear(By.XPATH, '//td[contains(text(), "an Example of title")]')
        texts = self.finds(By.CSS_SELECTOR, '#text_table tbody tr')
        self.assertEqual(len(texts), 1)
        text_row = texts[0]
        text_tds = text_row.find_elements_by_css_selector('td')
        if len(text_tds) == 1:
            self.wait_until_disappear(By.XPATH, '//td[contains(text(), "No matching records found")]')
        texts = self.finds(By.CSS_SELECTOR, '#text_table tbody tr')
        text_row = texts[0]
        text_tds = text_row.find_elements_by_css_selector('td')
        text_title = text_tds[5].text
        self.assertEqual(text_title, title_str)

        # creating a second text with tags:
        self.find(By.XPATH, '//a[@title="create a new text"]').click()
        select = Select(self.find(By.NAME,'language'))
        select.select_by_visible_text(self.language_1.name)
        title2_str = 'another title'
        title = self.find(By.NAME, 'title')
        title.send_keys(title2_str)
        text = self.find(By.NAME,'text')
        text.send_keys('And still another content for this text')
        wordtagarea = self.find(By.ID, 'id_texttags_tags_input_tag')
        wordtagarea.send_keys('testing')
        wordtagarea.send_keys(',')
        wordtagarea.send_keys('demo')
        wordtagarea.send_keys(',')
        save = self.find(By.ID, 'submit-id-save')
        save.click()

        self.selenium.get('{}/text_list/'.format(self.live_server_url))
        self.assertEqual(self.selenium.current_url, '{}/text_list/'.format(self.live_server_url))
#         self.find(By.CSS_SELECTOR, 'filterlangform input[value="1"]').click()
        self.find(By.CSS_SELECTOR, '#filterlangform input[value="2"]').click()
        self.wait_until_appear(By.XPATH, '//td[contains(text(), "another title")]')
        texts = self.finds(By.CSS_SELECTOR, '#text_table tbody tr')
        if len(texts) == 1:
            self.wait_until_disappear(By.XPATH, '//td[contains(text(), "No matching records found")]')
        texts = self.finds(By.CSS_SELECTOR, '#text_table tbody tr')
        self.assertEqual(len(texts), 2)
        text_row = texts[1]
        text_tds = text_row.find_elements_by_css_selector('td')
        text_title = text_tds[4].text
        self.assertEqual(text_title, title2_str+' [testing,demo]')
        
        
        
        
#     def test_create_wrong_text_symbol_content(self):  
#         self.selenium.get('{}/text_detail/new/0/'.format(self.live_server_url))
#         select = Select(self.find(By.NAME,'language'))
#         select.select_by_visible_text('German')
#         title = self.find(By.NAME, 'title')
#         title.send_keys('An Example of Title')
#         text = self.find(By.NAME,'text')
#         text.send_keys('1245. 78')
#         save = self.find(By.NAME, 'save')
#         save.click()
#         text_field = self.find(By.ID, 'div_id_text')
#         tf_class = text_field.get_attribute('class')
#         assert ('has-error' in text_field.get_attribute('class'))
#         title_field = self.find(By.ID, 'div_id_title')
#         assert ('has-error' not in title_field.get_attribute('class'))
#         
#     def test_create_wrong_text_blank_title(self):  
#         self.selenium.get('{}/text_detail/new/0/'.format(self.live_server_url))
#         select = Select(self.find(By.NAME,'language'))
#         title = self.find(By.NAME, 'title')
#         title.send_keys('')
#         text = self.find(By.NAME,'text')
#         text.send_keys('An example of content')
# 
#         save = self.find(By.NAME, 'save')
#         save.click()
#         text_field = self.find(By.ID, 'div_id_text')
#         assert ('has-error' not in text_field.get_attribute('class'))
#         title_field = self.find(By.ID, 'div_id_title')
#         assert ('has-error' in title_field.get_attribute('class'))
#         
#     def test_create_wrong_text_blank_text(self):  
#         self.selenium.get('{}/text_detail/new/0/'.format(self.live_server_url))
#         select = Select(self.find(By.NAME,'language'))
#         title = self.find(By.NAME, 'title')
#         title.send_keys('Example of title')
#         text = self.find(By.NAME,'text')
#         text.send_keys('')
#         save = self.find(By.NAME, 'save')
#         save.click()
#         text_field = self.find(By.ID, 'div_id_text')
#         assert ('has-error' in text_field.get_attribute('class'))
#         title_field = self.find(By.ID, 'div_id_title')
#         assert ('has-error' not in title_field.get_attribute('class'))
# 
#     def test_upload_text_file(self):  
#         self.selenium.get('{}/text_detail/?new=0/'.format(self.live_server_url))
#         myfile = open('Example_of_file_upload_title.txt', 'w+')
#         myfile.write('Example of content of file')
#         myfile.close()
#         myfile_path = os.path.join(os.getcwd(),'Example_of_file_upload_title.txt')
#         element = self.find(By.NAME, 'uploaded_text')
#         element.send_keys(myfile_path)
#         os.remove(myfile_path)
#         self.find(By.ID, 'submit-id-uploaded_text').click()
# 
#         self.wait_until(By.ID, 'text_table')
# #         wait = WebDriverWait(self.selenium, 10)
# #         wait.until(EC.presence_of_element_located(By.ID, 'text_table'))
# #         self.selenium.implicitly_wait(10)
# #         self.wait_until(By.ID, 'text_table')
#         self.selenium.get('{}/text_list/'.format(self.live_server_url))
#         self.assertEqual(self.selenium.current_url, '{}/text_list/'.format(self.live_server_url))
#         
# class Text_detail_no_js(BasePage_no_js):
# 
#     @classmethod
#     def setUpClass(cls):
#         super(Text_detail_no_js, cls).setUpClass()
#         cls.language_1 = GermanLanguagesFactory(owner=cls.user_1)
#         Settings_currentlang_idFactory(owner=cls.user_1, stvalue=cls.language_1.id)
#         cls.selenium.get('{}/accounts/login/'.format(cls.live_server_url))
#         cls.selenium.implicitly_wait(10)
#         login = cls.selenium.find_element_by_name('login')
#         login.send_keys(cls.user_1.username)
#         pw = cls.selenium.find_element_by_name('password')
#         pw.send_keys(cls.pwd)
#         cls.selenium.find_element_by_class_name('primaryAction').click()
# 
#     def test_create_wrong_text_symbol_content_no_js(self):  
#         self.selenium.get('{}/text_detail/new/0/'.format(self.live_server_url))
#         select = Select(self.find(By.NAME,'language'))
#         select.select_by_visible_text('German')
#         title = self.find(By.NAME, 'title')
#         title.send_keys('An Example of Title')
#         text = self.find(By.NAME,'text')
#         text.send_keys('1245. 78')
#         save = self.find(By.NAME, 'save')
#         save.click()
#         text_field = self.find(By.ID, 'div_id_text')
#         tf_class = text_field.get_attribute('class')
#         assert ('has-error' in text_field.get_attribute('class'))
#         title_field = self.find(By.ID, 'div_id_title')
#         assert ('has-error' not in title_field.get_attribute('class'))