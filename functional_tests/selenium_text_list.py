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
from lwt.models import Texts
from lwt.views._utilities_views import *
from selenium.webdriver.common import desired_capabilities
from .selenium_base import BasePage


class Text_list(BasePage):

    @classmethod
    def setUpClass(cls):
        super(Text_list, cls).setUpClass()
        cls.language_1 = GermanLanguagesFactory(owner=cls.user_1)
        Settings_currentlang_idFactory(owner=cls.user_1, stvalue=cls.language_1.id)
        cls.selenium.get('{}'.format(cls.live_server_url))
        cls.find(By.NAME, 'login').send_keys(cls.user_1.username)
        cls.find(By.NAME, 'password').send_keys(cls.pwd)
        cls.find(By.CSS_SELECTOR, "button[type='submit']").click()
 
    def tearDown(self):
        self.selenium.quit()
        super(Text_list, self).tearDown()
   
    def test_delete_a_text(self):  
        # create one text
        for i in range(2): # creating several texts
            self.selenium.get('{}/text_detail/?new=0/'.format(self.live_server_url))
            select = Select(self.find(By.NAME,'language'))
            select.select_by_visible_text('German')
            title = self.find(By.NAME, 'title')
            title.send_keys('An Example of Title_{}'.format(str(i)))
            text = self.find(By.NAME,'text')
            text.send_keys('This is the content of this text.')
            save = self.find(By.NAME, 'save')
            save.click()
            self.selenium.get('{}/text_list/'.format(self.live_server_url))
        #         text_1 = TextsFactory(owner=self.user_1)
        #         self.selenium.get('{}/text_list'.format(self.live_server_url))
        # than delete one of them:
        delCheckbox_css = (By.CSS_SELECTOR, 'input[name="btSelectItem"][data-index="0"]') 
#         self.wait_until_clickable(delCheckbox_css)
        self.find(*delCheckbox_css).click()

        self.find(By.CSS_SELECTOR, 'button[id="delete"]').click()
        
        delCheckbox2_css = (By.CSS_SELECTOR, 'input[id="delete_saved_words"]') 
#         self.wait_until_clickable(delCheckbox2_css)
        self.find(*delCheckbox2_css).click()
        buttonYes_selector = (By.XPATH, "//button[contains(text(),'Yes')]")
        self.find(*buttonYes_selector).click()
        
        title_td_selector = (By.XPATH, "//td[contains(text(),'An Example of Title_0')]")
        self.wait_until_disappear(*title_td_selector)
        self.assertTrue(self.selenium.find_elements(*title_td_selector) == [])

 

