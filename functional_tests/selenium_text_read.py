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
from lwt.models import MyUser
from lwt.views._utilities_views import *
from selenium.webdriver.common import desired_capabilities
from .selenium_base import BasePage

class Text_read(Base):

    def setUp(self):
        self.pwd = '12345'
        self.user_1 = UserFactory(password=self.pwd)
        self.selenium = WebDriver()
        super(Text_read, self).setUp()
        self.language_1 = GermanLanguagesFactory(owner=self.user_1)
        self.text1 = GermanTextsFactory(owner=self.user_1, language=self.language_1)
#         print(self.text1.text)
        splitText(self.text1)
        Settings_currentlang_idFactory(owner=self.user_1, stvalue=self.language_1.id)
        self.selenium.get('{}/accounts/login/'.format(self.live_server_url))
        self.selenium.implicitly_wait(10)
        login = self.selenium.find_element_by_name('login')
        login.send_keys(self.user_1.username)
        pw = self.selenium.find_element_by_name('password')
        pw.send_keys(self.pwd)
        self.selenium.find_element_by_class_name('primaryAction').click()

    def tearDown(self):
        self.selenium.quit()
        super(Text_read, self).tearDown()

#     @classmethod
#     def setUpClass(cls):
#         super(Text_read, cls).setUpClass()
#         cls.language_1 = GermanLanguagesFactory(owner=cls.user_1)
#         cls.text1 = GermanTextsFactory(owner=cls.user_1, language=cls.language_1)
#         print(cls.text1.text)
#         splitText(cls.text1)
#         Settings_currentlang_idFactory(owner=cls.user_1, stvalue=cls.language_1.id)
#         cls.selenium.get('{}/accounts/login/'.format(cls.live_server_url))
#         cls.selenium.implicitly_wait(10)
#         login = cls.selenium.find_element_by_name('login')
#         login.send_keys(cls.user_1.username)
#         pw = cls.selenium.find_element_by_name('password')
#         pw.send_keys(cls.pwd)
#         cls.selenium.find_element_by_class_name('primaryAction').click()

#     def test_go_to_text_read(self):
#         self.selenium.get('{}/text_read/{}'.format(self.live_server_url, self.text1.id))
#         time.sleep(5)
#         
#     def test_click_on_unknown_word(self):
#         self.selenium.get('{}/text_read/{}'.format(self.live_server_url, self.text1.id))
#         all_unknown_words = self.finds(By.XPATH, '//span[@wostatus=0]')
#         random_word = random.choice(all_unknown_words)
#         random_word.click()
#         print('Chosen word : ', random_word.text)
#         self.wait_until(By.CLASS_NAME, 'tooltiptext')
#         self.wait_until(By.XPATH, '//div[@id="bottomright"]/h3')
#         time.sleep(120)
# 
#     def test_click_show_similarword(self):
#         self.test_click_on_unknown_word()
#         self.find(By.XPATH, '//i[@href="#result_similarword"]').click()
#         self.wait_until(By.XPATH, '//div[@id="result_possiblesimilarword"]/p')
#         time.sleep(30)
# 
#     def test_click_on_unknown_word_dictwebpage(self):
#         language_2 = EnglishLanguagesFactory(owner=self.user_1)
#         Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
#         text2 = EnglishTextsFactory(owner=self.user_1, language=language_2)
#         splitText(text2)
#         self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
# 
#         all_unknown_words = self.finds(By.XPATH, '//span[@wostatus=0]')
#         random_word = random.choice(all_unknown_words)
#         random_word.click()
#         print('Chosen word : ', random_word.text)
#         self.wait_until(By.CLASS_NAME, 'tooltiptext')
#         self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
#         time.sleep(60)

    def test_saving_one_unknownword(self):
        language_2 = EnglishLanguagesFactory(owner=self.user_1)
        Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
        text2 = TextsFactory(owner=self.user_1, language=language_2, text='''
        This surplus will be carry over to the next season.
        Do you carry the surplus over?
        I like to carry this surplus''')
        splitText(text2)
        savedword = Words.objects.get(owner=self.user_1, wordtext="season")
        self.assertEqual(savedword.status, 0) # is unknown for the moment
        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
        word = self.find(By.XPATH, '//span[@wowordtext="season"]')
        self.assertEqual(word.get_attribute('title'), 'season\r▶Unknown [?]')
        word.click()
        self.wait_until(By.CLASS_NAME, 'tooltiptext')
        self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
        trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
        trans_textarea.send_keys('excédent')
        self.find(By.XPATH, '//button[@id="submit_word"]').click()
        self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')
        savedword = Words.objects.get(owner=self.user_1, wordtext="season")
        self.assertEqual(savedword.status, 1) # and now is 'Learning'
        word = self.find(By.XPATH, '//span[@wowordtext="season"]')
        self.assertEqual(word.get_attribute('title'), 'season\r▶ excédent\r▶ Learning [1]')
        
    def test_saving_one_unknownword_saves_all_the_others(self):
        language_2 = EnglishLanguagesFactory(owner=self.user_1)
        Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
        text2 = TextsFactory(owner=self.user_1, language=language_2, text='''
        This surplus will be carry over to the next season.
        Do you carry the surplus over?
        I like to carry this surplus''')
        splitText(text2)
        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))

        word = self.finds(By.XPATH, '//span[@wowordtext="surplus"]')
        word[0].click()
        self.wait_until(By.CLASS_NAME, 'tooltiptext')
        self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
        trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
        trans_textarea.send_keys('excédent')
        self.find(By.XPATH, '//button[@id="submit_word"]').click()
        self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')
        savedwords = Words.objects.filter(owner=self.user_1, wordtext="surplus", status=1).count()
        self.assertEqual(savedwords, 3)

    def test_saving_one_compoundword(self):
        language_2 = EnglishLanguagesFactory(owner=self.user_1)
        Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
        text2 = TextsFactory(owner=self.user_1, language=language_2, text='''
        Do you carry the surplus over?''')
        splitText(text2)
        # initial database
        first_word_DB_before = Words.objects.get( wordtext="carry")
        second_word_DB_before = Words.objects.get( wordtext="over")
        self.assertEqual(first_word_DB_before.compoundword, None) # and now is 'Learning'
        self.assertEqual(second_word_DB_before.compoundword, None) # and now is 'Learning'
        self.assertEqual(first_word_DB_before.status, 0) # it must not changed

        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
        first_word_before = self.find(By.XPATH, '//span[@wowordtext="carry"]')
        self.assertEqual(first_word_before.get_attribute('title'), 'carry\r▶Unknown [?]')
        first_word_before.click()
        self.wait_until(By.CLASS_NAME, 'tooltiptext')
        self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
        second_word_before = self.find(By.XPATH, '//span[@wowordtext="over"]')
        ActionChains(self.selenium).key_down(Keys.CONTROL).click(second_word_before).key_up(Keys.CONTROL).perform()

        self.wait_until(By.XPATH, '//textarea[@id="id_sentence"][contains(.,"{carry} the surplus {over}")]') 
        trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
        trans_textarea.send_keys('excédent')
        self.find(By.XPATH, '//button[@id="submit_word"]').click()
        self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')
        # good in database
        compoundword = Words.objects.get(isCompoundword=True, isnotword=True)
        self.assertEqual(compoundword.status, 1) # and now is 'Learning'
        first_word_DB_after = Words.objects.get( wordtext="carry")
        second_word_DB_after = Words.objects.get( wordtext="over")
        self.assertEqual(first_word_DB_after.compoundword, compoundword) # and now is 'Learning'
        self.assertEqual(second_word_DB_after.compoundword, compoundword) # and now is 'Learning'
        self.assertEqual(first_word_DB_after.show_compoundword, True) # and now is 'Learning'
        self.assertEqual(first_word_DB_after.status, 0) # it must not changed
        # and good css:
        firstword_after = self.find(By.XPATH, '//span[@wowordtext="carry"]')
        secondword_after = self.find(By.XPATH, '//span[@wowordtext="over"]')
        self.assertEqual(firstword_after.get_attribute('cowostatus'), '1')
        self.assertEqual(secondword_after.get_attribute('cowostatus'), '1')
        self.assertEqual(firstword_after.get_attribute('show_compoundword'), 'True')
        self.assertEqual(firstword_after.get_attribute('iscompoundword'), 'True')
        self.assertEqual(firstword_after.get_attribute('title'), 'carry\r▶ Unknown [?]\r• excédent\r• Learning [1]')
        
    def test_deleting_one_compoundword(self):
        language_2 = EnglishLanguagesFactory(owner=self.user_1)
        Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
        text2 = TextsFactory(owner=self.user_1, language=language_2, text='''
        Do you carry the surplus over?''')
        splitText(text2)
        first_word_inside = Words.objects.get( wordtext="carry")
        second_word_inside = Words.objects.get( wordtext="over")
        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
        first_word_before = self.find(By.XPATH, '//span[@wowordtext="carry"]')
        first_word_before.click()
        self.wait_until(By.CLASS_NAME, 'tooltiptext')
        self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
        second_word_before = self.find(By.XPATH, '//span[@wowordtext="over"]')
        ActionChains(self.selenium).key_down(Keys.CONTROL).click(second_word_before).key_up(Keys.CONTROL).perform()

        self.wait_until(By.XPATH, '//textarea[@id="id_sentence"][contains(.,"{carry} the surplus {over}")]') 
        
        trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
        trans_textarea.send_keys('excédent')
        self.wait_until(By.XPATH, '//button[@id="submit_word"]')
        self.find(By.XPATH, '//button[@id="submit_word"]').click()
        self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')

        # deleting the compound word:
        self.find(By.XPATH, '//span[@wowordtext="carry"]').click()

        self.find(By.XPATH, '//a[contains(.,"Delete term")]').click()
        self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: term deleted")]')

        compoundword = Words.objects.filter(isCompoundword=True, isnotword=True).all()
        self.assertEqual(len(compoundword), 0) # and now is 'Unknown'
        first_word_inside = Words.objects.get( wordtext="carry")
        second_word_inside = Words.objects.get( wordtext="over")
        self.assertEqual(first_word_inside.compoundword, None) # and now is 'Learning'
        self.assertEqual(second_word_inside.compoundword, None) # and now is 'Learning'
        self.assertEqual(first_word_inside.show_compoundword, False) # and now is 'Learning'
        # and good css:
        firstword_after = self.find(By.XPATH, '//span[@wowordtext="carry"]')
        secondword_after = self.find(By.XPATH, '//span[@wowordtext="over"]')
        self.assertEqual(firstword_after.get_attribute('cowostatus'), '0')
        self.assertEqual(secondword_after.get_attribute('cowostatus'), '0')
        self.assertEqual(firstword_after.get_attribute('show_compoundword'), 'False')
        self.assertEqual(firstword_after.get_attribute('iscompoundword'), 'False')
        self.assertEqual(firstword_after.get_attribute('title'), 'carry\r▶ Unknown [?]')

    def test_toggling_show_compoundword(self):
        language_2 = EnglishLanguagesFactory(owner=self.user_1)
        Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
        text2 = TextsFactory(owner=self.user_1, language=language_2, text='''
        Do you carry the surplus over?''')
        splitText(text2)

        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
        first_word_before = self.find(By.XPATH, '//span[@wowordtext="carry"]')
        first_word_before.click()
        self.wait_until(By.CLASS_NAME, 'tooltiptext')
        self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
        second_word_before = self.find(By.XPATH, '//span[@wowordtext="over"]')
        ActionChains(self.selenium).key_down(Keys.CONTROL).click(second_word_before).key_up(Keys.CONTROL).perform()

        self.wait_until(By.XPATH, '//textarea[@id="id_sentence"][contains(.,"{carry} the surplus {over}")]') 

        trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
        trans_textarea.send_keys('excédent')
        self.find(By.XPATH, '//button[@id="submit_word"]').click()
        self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')
        # in DB
        first_word_DB = Words.objects.get( wordtext="carry")
        second_word_DB = Words.objects.get( wordtext="over")
        self.assertEqual(first_word_DB.show_compoundword, True) 
        self.assertEqual(second_word_DB.show_compoundword, True) 
        
        # check untoggling 
        self.find(By.XPATH, '//span[@wowordtext="carry"]').click()
        self.find(By.XPATH, '//input[@name="show_compoundword_checkbox"]').click()
        # check the status of both words
        # in DB:
        first_word_DB = Words.objects.get( wordtext="carry")
        second_word_DB = Words.objects.get( wordtext="over")
        self.assertEqual(first_word_DB.show_compoundword, False) 
        self.assertEqual(second_word_DB.show_compoundword, False)
        # in HTML:
        first_word = self.find(By.XPATH, '//span[@wowordtext="carry"]')
        second_word = self.find(By.XPATH, '//span[@wowordtext="over"]')
        self.assertEqual(first_word.get_attribute('show_compoundword'), 'false')
        self.assertEqual(second_word.get_attribute('show_compoundword'), 'false')

        # and toggling again 
        self.find(By.XPATH, '//span[@wowordtext="carry"]').click()
        self.find(By.XPATH, '//input[@name="show_compoundword_checkbox"]').click()
        # check the status of both words
        # in DB:
        first_word_DB = Words.objects.get( wordtext="carry")
        second_word_DB = Words.objects.get( wordtext="over")
        self.assertEqual(first_word_DB.show_compoundword, True) 
        self.assertEqual(second_word_DB.show_compoundword, True)
        # in HTML:
        first_word = self.find(By.XPATH, '//span[@wowordtext="carry"]')
        second_word = self.find(By.XPATH, '//span[@wowordtext="over"]')
        self.assertEqual(first_word.get_attribute('show_compoundword'), 'true')
        self.assertEqual(second_word.get_attribute('show_compoundword'), 'true')