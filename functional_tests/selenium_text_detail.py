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
from .selenium_base import BasePage, BasePage_no_js

class Text_detail(BasePage):

    @classmethod
    def setUpClass(cls):
        super(Text_detail, cls).setUpClass()
        cls.language_1 = GermanLanguagesFactory(owner=cls.user_1)
        Settings_currentlang_idFactory(owner=cls.user_1, stvalue=cls.language_1.id)
        cls.selenium.get('{}'.format(cls.live_server_url))
        cls.find(By.NAME, 'login').send_keys(cls.user_1.username)
        cls.find(By.NAME, 'password').send_keys(cls.pwd)
        cls.find(By.CSS_SELECTOR, "button[type='submit']").click()

    def test_create_a_new_text(self):  
        language_1 = LanguagesFactory(owner=self.user_1)
        self.selenium.get('{}/text_detail/?new=0/'.format(self.live_server_url))
        select = Select(self.find(By.NAME,'language'))
        select.select_by_visible_text('German')
        title = self.find(By.NAME, 'title')
        title.send_keys('An Example of Title')
        text = self.find(By.NAME,'text')
        text.send_keys('This is the content of this text.')
        save = self.find(By.NAME, 'save')
        save.click()
        time.sleep(5)
#         self.selenium.implicitly_wait(10)
#         self.wait_until(By.ID, 'text_table')
        self.selenium.get('{}/text_list/'.format(self.live_server_url))
        self.assertEqual(self.selenium.current_url, '{}/text_list/'.format(self.live_server_url))

    def test_create_wrong_text_symbol_content(self):  
        self.selenium.get('{}/text_detail/new/0/'.format(self.live_server_url))
        select = Select(self.find(By.NAME,'language'))
        select.select_by_visible_text('German')
        title = self.find(By.NAME, 'title')
        title.send_keys('An Example of Title')
        text = self.find(By.NAME,'text')
        text.send_keys('1245. 78')
        save = self.find(By.NAME, 'save')
        save.click()
        text_field = self.find(By.ID, 'div_id_text')
        tf_class = text_field.get_attribute('class')
        assert ('has-error' in text_field.get_attribute('class'))
        title_field = self.find(By.ID, 'div_id_title')
        assert ('has-error' not in title_field.get_attribute('class'))
        
    def test_create_wrong_text_blank_title(self):  
        self.selenium.get('{}/text_detail/new/0/'.format(self.live_server_url))
        select = Select(self.find(By.NAME,'language'))
        title = self.find(By.NAME, 'title')
        title.send_keys('')
        text = self.find(By.NAME,'text')
        text.send_keys('An example of content')

        save = self.find(By.NAME, 'save')
        save.click()
        text_field = self.find(By.ID, 'div_id_text')
        assert ('has-error' not in text_field.get_attribute('class'))
        title_field = self.find(By.ID, 'div_id_title')
        assert ('has-error' in title_field.get_attribute('class'))
        
    def test_create_wrong_text_blank_text(self):  
        self.selenium.get('{}/text_detail/new/0/'.format(self.live_server_url))
        select = Select(self.find(By.NAME,'language'))
        title = self.find(By.NAME, 'title')
        title.send_keys('Example of title')
        text = self.find(By.NAME,'text')
        text.send_keys('')
        save = self.find(By.NAME, 'save')
        save.click()
        text_field = self.find(By.ID, 'div_id_text')
        assert ('has-error' in text_field.get_attribute('class'))
        title_field = self.find(By.ID, 'div_id_title')
        assert ('has-error' not in title_field.get_attribute('class'))

    def test_upload_text_file(self):  
        self.selenium.get('{}/text_detail/?new=0/'.format(self.live_server_url))
        myfile = open('Example_of_file_upload_title.txt', 'w+')
        myfile.write('Example of content of file')
        myfile.close()
        myfile_path = os.path.join(os.getcwd(),'Example_of_file_upload_title.txt')
        element = self.find(By.NAME, 'uploaded_text')
        element.send_keys(myfile_path)
        os.remove(myfile_path)
        self.find(By.ID, 'submit-id-uploaded_text').click()

        self.wait_until(By.ID, 'text_table')
#         wait = WebDriverWait(self.selenium, 10)
#         wait.until(EC.presence_of_element_located(By.ID, 'text_table'))
#         self.selenium.implicitly_wait(10)
#         self.wait_until(By.ID, 'text_table')
        self.selenium.get('{}/text_list/'.format(self.live_server_url))
        self.assertEqual(self.selenium.current_url, '{}/text_list/'.format(self.live_server_url))
        
class Text_detail_no_js(BasePage_no_js):

    @classmethod
    def setUpClass(cls):
        super(Text_detail_no_js, cls).setUpClass()
        cls.language_1 = GermanLanguagesFactory(owner=cls.user_1)
        Settings_currentlang_idFactory(owner=cls.user_1, stvalue=cls.language_1.id)
        cls.selenium.get('{}/accounts/login/'.format(cls.live_server_url))
        cls.selenium.implicitly_wait(10)
        login = cls.selenium.find_element_by_name('login')
        login.send_keys(cls.user_1.username)
        pw = cls.selenium.find_element_by_name('password')
        pw.send_keys(cls.pwd)
        cls.selenium.find_element_by_class_name('primaryAction').click()

    def test_create_wrong_text_symbol_content_no_js(self):  
        self.selenium.get('{}/text_detail/new/0/'.format(self.live_server_url))
        select = Select(self.find(By.NAME,'language'))
        select.select_by_visible_text('German')
        title = self.find(By.NAME, 'title')
        title.send_keys('An Example of Title')
        text = self.find(By.NAME,'text')
        text.send_keys('1245. 78')
        save = self.find(By.NAME, 'save')
        save.click()
        text_field = self.find(By.ID, 'div_id_text')
        tf_class = text_field.get_attribute('class')
        assert ('has-error' in text_field.get_attribute('class'))
        title_field = self.find(By.ID, 'div_id_title')
        assert ('has-error' not in title_field.get_attribute('class'))