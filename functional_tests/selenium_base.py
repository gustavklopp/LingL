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


class Base(StaticLiveServerTestCase):

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super(Base, cls).tearDownClass()

#     @classmethod
#     def find(cls, findhow, findwhere): # wait until and find
#         cls.wait_until_appear(findhow, findwhere)
#         return cls.selenium.find_element(findhow, findwhere)
# 
#     @classmethod
#     def finds(cls, findhow, findwhere): # wait until and find
#         cls.wait_until_appear(findhow, findwhere)
#         return cls.selenium.find_elements(findhow, findwhere)
# 
#     @classmethod
#     def wait_until_appear(cls, findhow, findwhere):
#         WebDriverWait(cls.selenium, 30).until(
#             EC.presence_of_element_located((findhow,findwhere))
#             )
# 
#     @classmethod
#     def wait_until_disappear(cls, findhow, findwhere):
#         WebDriverWait(cls.selenium, 30).until(
#             EC.invisibility_of_element_located((findhow,findwhere))
#             )
# 
#     @classmethod
#     def wait_until_clickable(cls, element_selector):
#         WebDriverWait(cls.selenium, 30).until(
#             EC.element_to_be_clickable(element_selector)
#             )
# 
#     @classmethod
#     def wait_until_text_appear(cls, element_selector, text):
#         WebDriverWait(cls.selenium, 30).until(
#             EC.text_to_be_present_in_element(element_selector, text)
#             )

    def find(self, findhow, findwhere): # wait until and find
        self.wait_until_appear(findhow, findwhere)
        return self.selenium.find_element(findhow, findwhere)

    def finds(self, findhow, findwhere): # wait until and find
        self.wait_until_appear(findhow, findwhere)
        return self.selenium.find_elements(findhow, findwhere)

    def wait_until_appear(self, findhow, findwhere):
        WebDriverWait(self.selenium, 30).until(
            EC.presence_of_element_located((findhow,findwhere))
            )

    def wait_until_disappear(self, findhow, findwhere):
        WebDriverWait(self.selenium, 30).until(
            EC.invisibility_of_element_located((findhow,findwhere))
            )

    def wait_until_clickable(self, element_selector):
        WebDriverWait(self.selenium, 30).until(
            EC.element_to_be_clickable(element_selector)
            )

    def wait_until_text_appear(self, element_selector, text):
        WebDriverWait(self.selenium, 30).until(
            EC.text_to_be_present_in_element(element_selector, text)
            )

    def wait_until_bool(self, element_selector, text):
        WebDriverWait(self.selenium, 30).until(
            EC.text_to_be_present_in_element(element_selector, text)
            )
class BasePage(Base):

    @classmethod
    def setUpClass(cls):
        cls.pwd = 'selenium20171106!!!'
        cls.user_1 = UserFactory(password=cls.pwd)
        cls.selenium = WebDriver()
        super(Base, cls).setUpClass()

class BasePage_loggedin(Base):

    @classmethod
    def setUpClass(cls):
        cls.pwd = '12345'
        cls.user_1 = UserFactory(password=cls.pwd, origin_lang_code='en')
        super(BasePage_loggedin, cls).setUpClass()

#         cls.selenium = WebDriver()
        cls.selenium = WebDriver()
#         cls.client = Client()
#         cls.user_1 = MyUser.objects.create_user(cls.user_1.username,password='12345')
#         cls.client.force_login(cls.user_1)
#         cls.client.login(username=cls.user_1.username, password=cls.user_1.password)
#         cls.client.login(username=cls.user_1.username, password=cls.pwd)
        
        # create session cookie:
#         session = SessionStore()
#         session[SESSION_KEY] = cls.user_1.pk
#         session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
#         session[HASH_SESSION_KEY] = cls.user_1.get_session_auth_hash()
#         session.save()
# 
#         # Finally, create the cookie dictionary
#         cookie = {
#             'name': settings.SESSION_COOKIE_NAME,
#             'value': session.session_key,
#             'secure': False,
#             'path': '/',
#         }
# #         cookie = cls.client.cookies['sessionid']
        cls.selenium.get('{}'.format(cls.live_server_url))
#         cls.selenium.add_cookie(cookie)
#         cls.selenium.add_cookie({'name':'sessionid', 'value': cookie.value, 'secure':False, 'path':'/'})
        cls.find(By.NAME, 'login').send_keys(cls.user_1.username)
        cls.find(By.NAME, 'password').send_keys(cls.pwd)
        cls.find(By.CSS_SELECTOR, "button[type='submit']").click()
#         cls.selenium.implicitly_wait(10)
#         cls.selenium.refresh()
#         cls.selenium.get('{}'.format(cls.live_server_url))
#         response = cls.client.get('{}/language_detail?new=0'.format(cls.live_server_url))


class BasePage_no_js(Base): # same than above but disable Javascript

    @classmethod
    def setUpClass(cls):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('javascript.enabled', False)

        cls.pwd = 'selenium20171106!!!'
        cls.user_1 = UserFactory(password=cls.pwd)
        cls.selenium = WebDriver(profile)
        super(Base, cls).setUpClass()
    
class TestSignUp(Base):  

    @classmethod
    def setUpClass(cls):
        cls.pwd = 'selenium20171106!!!'
        cls.username ='JohnDOe'
        super(TestSignUp, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.get('{}/accounts/signup/?next=%2F'.format(cls.live_server_url))
        login = cls.find(By.ID, 'id_username')
        login.send_keys(cls.username)
        pw = cls.find(By.ID, 'id_password1')
        pw.send_keys(cls.pwd)
        pw = cls.find(By.ID, 'id_password2')
        pw.send_keys(cls.pwd)
        select = Select(cls.find(By.NAME,'origin_lang_code'))
        select.select_by_visible_text('German')
        cls.find(By.ID, 'submit-id-signup').click()

    def test_signup(self):
        user = MyUser.objects.get(username=self.username)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.origin_lang_code, 'de')

    def test_loggout(self):
        self.selenium.get(self.live_server_url) # return 'localhost:8000
        self.selenium.find_element_by_name('logout').click()
        self.selenium.get('{}/accounts/logout/'.format(self.live_server_url))
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

class Selenium(Base):  

    @classmethod
    def setUpClass(cls):
        cls.pwd = 'selenium20171106!!!'
        cls.user_1 = UserFactory(password=cls.pwd)
        cls.language_1 = LanguagesFactory(owner=cls.user_1)
        Settings_currentlang_idFactory(owner=cls.user_1, stvalue=cls.language_1.id)
        super(Selenium, cls).setUpClass()
        cls.selenium = WebDriver()
#         cls.selenium.get('{}'.format(cls.live_server_url))
        cls.selenium.get('{}/accounts/login'.format(cls.live_server_url))
        login = cls.find(By.ID, 'id_username')
        login.send_keys(cls.user_1.username)
        pw = cls.find(By.ID, 'id_password1')
        pw.send_keys(cls.pwd)
        pw = cls.find(By.ID, 'id_password2')
        pw.send_keys(cls.pwd)
        select = Select(cls.find(By.NAME,'origin_lang_code'))
        select.select_by_visible_text('German')
        cls.find(By.ID, 'submit-id-signup').click()

    def test_signup(self):
        pass

    def test_go_to_homepage(self):  
        self.selenium.get(self.live_server_url) # return 'localhost:8000

    def test_go_to_text_list(self):
        self.language_1 = LanguagesFactory(owner=self.user_1)
        Settings_currentlang_idFactory(owner=self.user_1, stvalue=self.language_1.id)
        text1 = TextsFactory(owner=self.user_1, language=self.language_1)
        self.selenium.get('{}/text_list/'.format(self.live_server_url))
        

class Selenium_old_lwt(StaticLiveServerTestCase):  
    ''' it tests with the fixture from "old_lwt' (the non opensource version)'''

    fixtures = ['lwt/fixtures/old_lwt.json']

    def setUp(self):
        self.pwd = '12345'
        self.user_1 = User.objects.get(username='oldlwt')
        self.language_1 = Languages.objects.get(name='Italian')
        
        Settings_currentlang_idFactory(owner=self.user_1, stvalue=self.language_1.id)
        super(Selenium_old_lwt, self).setUpClass()
        self.selenium = WebDriver()
        self.selenium.get('{}/accounts/login/'.format(self.live_server_url))
        self.selenium.implicitly_wait(10)
        login = self.selenium.find_element_by_name('login')
        login.send_keys(self.user_1.username)
        pw = self.selenium.find_element_by_name('password')
        pw.send_keys(self.pwd)
        self.selenium.find_element_by_class_name('primaryAction').click()

    def test_loggout(self):
        self.selenium.get(self.live_server_url) # return 'localhost:8000
        self.selenium.find_element_by_name('logout').click()
        self.selenium.get('{}/accounts/logout/'.format(self.live_server_url))
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

    def tearDown(self):
#         self.selenium.quit()
        super(Selenium_old_lwt, self).tearDown()
        
    def test_go_to_homepage(self):  
        self.selenium.get(self.live_server_url) # return 'localhost:8000

    def test_go_to_text_list(self):
        self.selenium.get('{}/text_list/'.format(self.live_server_url))

    def test_go_to_text_read(self):
        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, self.text1.id))
