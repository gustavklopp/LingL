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

class Text_read(Base):

    def setUp(self):
        super(Text_read, self).setUp()
        self.pwd = 'selenium12345!!!'
        self.user_1 = UserFactory(password=self.pwd)
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
        super(Text_read, self).tearDown()

#     @classmethod
#     def setUpClass(cls):
#         super(Text_read, cls).setUpClass()
#         cls.pwd = 'selenium20171106!!!'
#         cls.user_1 = UserFactory(password=cls.pwd)
#         cls.selenium = WebDriver()
#         cls.language_1 = EnglishLanguagesFactory(owner=cls.user_1)
# #         cls.text1 = GermanTextsFactory(owner=cls.user_1, language=cls.language_1)
# #         print(cls.text1.text)
# #         splitText(cls.text1)
#         Settings_currentlang_idFactory(owner=cls.user_1, stvalue=cls.language_1.id)
#         cls.selenium.get('{}'.format(cls.live_server_url))
#         cls.find(By.NAME, 'login').send_keys(cls.user_1.username)
#         cls.find(By.NAME, 'password').send_keys(cls.pwd)
#         cls.find(By.CSS_SELECTOR, "button[type='submit']").click()

#         language_2 = LanguagesFactory(owner=cls.user_1)
#         Settings_currentlang_id.objects.get(owner=cls.user_1).stvalue=language_2

#     def test_go_to_text_read(self):
#         self.selenium.get('{}/text_read/{}'.format(self.live_server_url, self.text1.id))
         
#     def test_click_on_unknown_word(self):
#         self.selenium.get('{}/text_read/{}'.format(self.live_server_url, self.text1.id))
#         all_unknown_words = self.finds(By.XPATH, '//span[@wostatus=0]')
#         random_word = random.choice(all_unknown_words)
#         random_word.click()
#         print('Chosen word : ', random_word.text)
#         self.wait_until(By.CLASS_NAME, 'tooltiptext')
#         self.wait_until(By.XPATH, '//div[@id="bottomright"]/h3')
#         time.sleep(120)
 
    def test_save_word_with_similarity(self):
#         language_2 = LanguagesFactory(owner=self.user_1)
#         Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
        text2 = TextsFactory(owner=self.user_1, language=self.language_1)
        sentence1 ='AAA BBB AAA AAA BBB.\n' 
        text2.text = sentence1
        sentence2 = 'VVV DDD VVV DDD EEE RRR TTT UUU EEE EEE TTT OOO.\n'
        text2.text += sentence2
        sentence3 = 'PPP LLL PPP MMM NNN OOO MMM LLL MMM NNN.'
        text2.text += sentence3

        # Verify that the splitting text is working
        splitText(text2)
        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
        thetext = self.find(By.ID, "thetext")
        self.assertEqual(text2.text.strip(), thetext.text.strip(), msg='Text on the text_read screen is not what the new text when created')
        
        # when using move_to_element, we MUST use 'click()' after (even if not needed to click...)
#         tooltip_righthandle_selector = (By.XPATH, "//td[contains(text(),'Close')]") 
#         tooltip_righthandle = self.find(*tooltip_righthandle_selector) 
#         ActionChains(self.selenium).move_to_element(tooltip_righthandle).click().perform()
#         self.wait_until_disappear(*tooltip_righthandle_selector)
#         self.assertEqual(len(self.selenium.find_elements(*tooltip_righthandle_selector)), 0, 
#                          msg="Tooltip doesn't disappear when mouse over the right handle")
# 
        self.wait_until_appear(By.CSS_SELECTOR, 'iframe[id="dictwebpage"]')
        words = self.finds(By.XPATH, "//span[contains(text(),'MMM')]")
        words[0].click()
 
        # verify that new_term_form is created in the top right and submit a translation
        expected_sent = sentence3.replace('MMM', '**MMM**')
        self.wait_until_appear(By.XPATH, "//textarea[@id='id_sentence' and contains(text(), '{}')]".format(expected_sent))
        textarea = self.find(By.ID, 'id_translation')
        textarea.send_keys('a')
        self.find(By.ID, 'submit_word').click()
        elements = self.finds(By.CSS_SELECTOR, 'span[wostatus="1"')
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0].text, 'MMM')
        
        # creating a new text with the same words:
        text3 = TextsFactory(owner=self.user_1, language=self.language_1)
        text3.text = text2.text
        splitText(text3)
        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text3.id))
 
        # when using move_to_element, we MUST use 'click()' after (even if not needed to click...)
#         tooltip_righthandle_selector = (By.XPATH, "//td[contains(text(),'Close')]") 
#         tooltip_righthandle = self.find(*tooltip_righthandle_selector) 
#         ActionChains(self.selenium).move_to_element(tooltip_righthandle).click().perform()
#         self.wait_until_disappear(*tooltip_righthandle_selector)
#         self.assertEqual(len(self.selenium.find_elements(*tooltip_righthandle_selector)), 0, 
#                          msg="Tooltip doesn't disappear when mouse over the right handle")
# 
        elements = self.finds(By.CSS_SELECTOR, 'span[wostatus="1"')
        self.assertEqual(len(elements), 3, msg="New text don't get the already saved words")
        self.assertEqual(elements[0].text, 'MMM')
        
        #editing a word translation:
        elements[0].click()
        self.wait_until_appear(By.CLASS_NAME, 'tooltiptext')
        self.find(By.XPATH, "//a[contains(text(),'Edit term')]").click()
        submit = self.find(By.XPATH, "//button[@id='submit_word' and contains(text(),'Change')]")
        textarea = self.find(By.ID, 'id_translation')
        textarea.clear()
        textarea.send_keys('b')
        submit.click()
        elements[2].click()
        tooltip = self.find(By.CLASS_NAME, 'tooltiptext')
        self.assertTrue('▶ b' in tooltip.text)
        
        #editing a word status to 'well-known':
        tooltip_righthandle_selector = (By.XPATH, '//td[@align="RIGHT"]/a') 
        tooltip_righthandle = self.find(*tooltip_righthandle_selector) 
        ActionChains(self.selenium).move_to_element(tooltip_righthandle).click().perform()
        self.wait_until_disappear(*tooltip_righthandle_selector)

        elements[1].click()
        self.wait_until_appear(By.CLASS_NAME, 'tooltiptext')
        self.find(By.XPATH, "//a[contains(text(),'Edit term')]").click()
        submit = self.find(By.XPATH, "//button[@id='submit_word' and contains(text(),'Change')]")
        textarea = self.find(By.ID, 'id_translation')
        textarea.clear()
        textarea.send_keys('c')
        # changing status to well known
        self.find(By.CSS_SELECTOR, 'input[value="100"]').click()
        submit.click()
        elements = self.finds(By.XPATH, '//span[@wostatus="100" and contains(text(),"MMM")]')
        self.assertEqual(len(elements), 3)
        
        # and changing again the status 'well-known' to learning:
        elements[2].click()
        self.wait_until_appear(By.CLASS_NAME, 'tooltiptext')
        self.find(By.XPATH, "//a[contains(text(),'Edit term')]").click()
        submit = self.find(By.XPATH, "//button[@id='submit_word' and contains(text(),'Change')]")
        textarea = self.find(By.ID, 'id_translation')
        textarea.clear()
        textarea.send_keys('d')
        # changing status to well known
        self.find(By.CSS_SELECTOR, 'input[value="1"]').click()
        submit.click()
        elements = self.finds(By.XPATH, '//span[@wostatus="1" and contains(text(),"MMM")]')
        self.assertEqual(len(elements), 3)
        
    def test_submit_similar_word(self):
#         language_3 = LanguagesFactory(owner=self.user_1)
#         Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_3
        text2 = TextsFactory(owner=self.user_1, language=self.language_1)
        sentences ='''aimer aimerais aimeront aimant aimer.
                       aimerais aimable aimable.'''
        text2.text = sentences
        splitText(text2)
        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
 
        self.wait_until_appear(By.CSS_SELECTOR, 'iframe[id="dictwebpage"]')
        
        # moving on the 'x' of the tooltip makes it disappear
        tooltip_righthandle_selector = (By.XPATH, '//td[@align="RIGHT"]/a') 
        tooltip_righthandle = self.find(*tooltip_righthandle_selector) 
        ActionChains(self.selenium).move_to_element(tooltip_righthandle).click().perform()
        self.wait_until_disappear(*tooltip_righthandle_selector)
        self.assertEqual(self.selenium.find_element(*tooltip_righthandle_selector).text, '', 
                         msg="Tooltip doesn't disappear when mouse over the right handle")
 
        # submit the word 'aimer'
        words_aimer = self.finds(By.XPATH, "//span[contains(text(),'aimer')]")
        words_aimer[0].click()
        textarea = self.find(By.ID, 'id_translation')
        textarea.send_keys('to love')

        self.find(By.ID, 'submit_word').click()

        self.wait_until_text_appear((By.XPATH, '//div[@id="topright"]'), 'OK: Term saved.')
        
        # then click on another word: 'aimerais' in text_read
        words_aimerais = self.finds(By.XPATH, "//span[contains(text(),'aimerais')]")
        words_aimerais[0].click()
        # click on the similar word (word already saved)
        similarwords = self.finds(By.XPATH, '//span[@class="possible_similarword"]')
        self.assertEqual(len(similarwords), 1)
        similarwords[0].click()
        totalsavedwords = self.finds(By.XPATH, '//span[@wostatus="1"]')
        self.assertEqual(len(totalsavedwords), 4)
        newsavedwords = self.finds(By.XPATH, '//span[@wostatus="1" and contains(text(), "aimerais")]')
        self.assertEqual(len(newsavedwords), 2)
        
        # create a new text with the same text
        text3 = TextsFactory(owner=self.user_1, language=self.language_1)
        text3.text = text2.text
        splitText(text3)
        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text3.id))
 
        # when using move_to_element, we MUST use 'click()' after (even if not needed to click...)
#         tooltip_righthandle_selector = (By.XPATH, "//td[contains(text(),'Close')]") 
#         tooltip_righthandle = self.find(*tooltip_righthandle_selector) 
#         ActionChains(self.selenium).move_to_element(tooltip_righthandle).click().perform()
#         self.wait_until_disappear(*tooltip_righthandle_selector)
#         self.assertEqual(len(self.selenium.find_elements(*tooltip_righthandle_selector)), 0, 
#                          msg="Tooltip doesn't disappear when mouse over the right handle")

        totalsavedwords = self.finds(By.XPATH, '//span[@wostatus="1"]')
        self.assertEqual(len(totalsavedwords), 4)
        newsavedwords = self.finds(By.XPATH, '//span[@wostatus="1" and contains(text(), "aimerais")]')
        self.assertEqual(len(newsavedwords), 2, )

        # clicking on word 'aimeront' should make only one similar word to appear:
        words = self.finds(By.XPATH, "//span[contains(text(),'aimeront')]")
        words[0].click()
        similarwords = self.finds(By.XPATH, '//span[@class="possible_similarword"]')
        self.assertEqual(len(similarwords), 1)
        
        #editing a word make all similar words updated:
        tooltip_righthandle_selector = (By.XPATH, '//td[@align="RIGHT"]/a') 
        tooltip_righthandle = self.find(*tooltip_righthandle_selector) 
        ActionChains(self.selenium).move_to_element(tooltip_righthandle).click().perform()
        self.wait_until_disappear(*tooltip_righthandle_selector)

        self.finds(By.XPATH, '//span[@wostatus="1" and contains(text(), "aimerais")]')[1].click()
        self.wait_until_appear(By.CLASS_NAME, 'tooltiptext')
        self.find(By.XPATH, "//a[contains(text(),'Edit term')]").click()
        submit = self.find(By.XPATH, "//button[@id='submit_word' and contains(text(),'Change')]")
        textarea = self.find(By.ID, 'id_translation')
        textarea.clear()
        textarea.send_keys('to hate')
        submit.click()
        self.finds(By.XPATH, '//span[@wostatus="1" and contains(text(), "aimer")]')[1].click()
        tooltip = self.find(By.CLASS_NAME, 'tooltiptext')
        self.assertTrue('▶ to hate' in tooltip.text)

    def test_saving_one_compoundword(self):
#         language_2 = EnglishLanguagesFactory(owner=self.user_1)
#         Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
        text2 = TextsFactory(owner=self.user_1, language=self.language_1, text='''
        Do you carry the surplus over?
it is over. the carry. the carry is well over. 
is over the carry?''')
        splitText(text2)
        # initial database
        first_word_DB_before = Words.objects.filter( wordtext="carry").first()
        second_word_DB_before = Words.objects.filter( wordtext="over").first()
        self.assertEqual(first_word_DB_before.compoundword, None) 
        self.assertEqual(second_word_DB_before.compoundword, None)
        self.assertEqual(first_word_DB_before.status, 0) 
 
        self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
        first_word_before = self.find(By.XPATH, '//span[@wowordtext="carry"]')
        self.assertEqual(first_word_before.get_attribute('title'), 'carry\r▶ Unknown [0]')
        first_word_before.click()
        self.wait_until_appear(By.CLASS_NAME, 'tooltiptext')
        self.wait_until_appear(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
        second_word_before = self.find(By.XPATH, '//span[@wowordtext="over"]')
        # ctrl+click the second word
        ActionChains(self.selenium).key_down(Keys.CONTROL).click(second_word_before).key_up(Keys.CONTROL).perform()
 
        self.wait_until_appear(By.XPATH, '//textarea[@id="id_sentence"][contains(.,"Do you **carry** the surplus **over**?")]') 
        trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
        trans_textarea.send_keys('excédent')
        self.find(By.XPATH, '//button[@id="submit_word"]').click()
        self.wait_until_appear(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')
        # good in database
        compoundword = Words.objects.get(isCompoundword=True, isnotword=True)
        self.assertEqual(compoundword.status, 1) # and now is 'Learning'
        first_word_DB_after = Words.objects.filter( wordtext="carry").first()
        second_word_DB_after = Words.objects.filter( wordtext="over").first()
        self.assertEqual(first_word_DB_after.compoundword, compoundword) # and now is 'Learning'
        self.assertEqual(second_word_DB_after.compoundword, compoundword) # and now is 'Learning'
        self.assertEqual(first_word_DB_after.show_compoundword, True) # and now is 'Learning'
        self.assertEqual(first_word_DB_after.status, 0) # it must not changed
        # and good css:
        firstword_after = self.find(By.XPATH, '//span[@wowordtext="carry" and @cowordtext="carry+over"]')
        secondword_after = self.find(By.XPATH, '//span[@wowordtext="over" and @cowordtext="carry+over"]')
        self.assertEqual(firstword_after.get_attribute('cowostatus'), '1')
        self.assertEqual(secondword_after.get_attribute('cowostatus'), '1')
        self.assertEqual(firstword_after.get_attribute('show_compoundword'), 'True')
        self.assertEqual(firstword_after.get_attribute('iscompoundword'), 'True')
        self.assertEqual(firstword_after.get_attribute('title'), 'carry+over\r• excédent\r• Learning [1]')
 
    ####### FUNCTIONS BELOW TO BE CHECKED ###########

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
# 
#     def test_saving_one_unknownword(self):
#         language_2 = EnglishLanguagesFactory(owner=self.user_1)
#         Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
#         text2 = TextsFactory(owner=self.user_1, language=language_2, text='''
#         This surplus will be carry over to the next season.
#         Do you carry the surplus over?
#         I like to carry this surplus''')
#         splitText(text2)
#         savedword = Words.objects.get(owner=self.user_1, wordtext="season")
#         self.assertEqual(savedword.status, 0) # is unknown for the moment
#         self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
#         word = self.find(By.XPATH, '//span[@wowordtext="season"]')
#         self.assertEqual(word.get_attribute('title'), 'season\r▶Unknown [?]')
#         word.click()
#         self.wait_until(By.CLASS_NAME, 'tooltiptext')
#         self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
#         trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
#         trans_textarea.send_keys('excédent')
#         self.find(By.XPATH, '//button[@id="submit_word"]').click()
#         self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')
#         savedword = Words.objects.get(owner=self.user_1, wordtext="season")
#         self.assertEqual(savedword.status, 1) # and now is 'Learning'
#         word = self.find(By.XPATH, '//span[@wowordtext="season"]')
#         self.assertEqual(word.get_attribute('title'), 'season\r▶ excédent\r▶ Learning [1]')
#         
#     def test_saving_one_unknownword_saves_all_the_others(self):
#         language_2 = EnglishLanguagesFactory(owner=self.user_1)
#         Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
#         text2 = TextsFactory(owner=self.user_1, language=language_2, text='''
#         This surplus will be carry over to the next season.
#         Do you carry the surplus over?
#         I like to carry this surplus''')
#         splitText(text2)
#         self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
# 
#         word = self.finds(By.XPATH, '//span[@wowordtext="surplus"]')
#         word[0].click()
#         self.wait_until(By.CLASS_NAME, 'tooltiptext')
#         self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
#         trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
#         trans_textarea.send_keys('excédent')
#         self.find(By.XPATH, '//button[@id="submit_word"]').click()
#         self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')
#         savedwords = Words.objects.filter(owner=self.user_1, wordtext="surplus", status=1).count()
#         self.assertEqual(savedwords, 3)
# 
         
#     def test_deleting_one_compoundword(self):
#         language_2 = EnglishLanguagesFactory(owner=self.user_1)
#         Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
#         text2 = TextsFactory(owner=self.user_1, language=language_2, text='''
#         Do you carry the surplus over?''')
#         splitText(text2)
#         first_word_inside = Words.objects.get( wordtext="carry")
#         second_word_inside = Words.objects.get( wordtext="over")
#         self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
#         first_word_before = self.find(By.XPATH, '//span[@wowordtext="carry"]')
#         first_word_before.click()
#         self.wait_until(By.CLASS_NAME, 'tooltiptext')
#         self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
#         second_word_before = self.find(By.XPATH, '//span[@wowordtext="over"]')
#         ActionChains(self.selenium).key_down(Keys.CONTROL).click(second_word_before).key_up(Keys.CONTROL).perform()
# 
#         self.wait_until(By.XPATH, '//textarea[@id="id_sentence"][contains(.,"{carry} the surplus {over}")]') 
#         
#         trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
#         trans_textarea.send_keys('excédent')
#         self.wait_until(By.XPATH, '//button[@id="submit_word"]')
#         self.find(By.XPATH, '//button[@id="submit_word"]').click()
#         self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')
# 
#         # deleting the compound word:
#         self.find(By.XPATH, '//span[@wowordtext="carry"]').click()
# 
#         self.find(By.XPATH, '//a[contains(.,"Delete term")]').click()
#         self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: term deleted")]')
# 
#         compoundword = Words.objects.filter(isCompoundword=True, isnotword=True).all()
#         self.assertEqual(len(compoundword), 0) # and now is 'Unknown'
#         first_word_inside = Words.objects.get( wordtext="carry")
#         second_word_inside = Words.objects.get( wordtext="over")
#         self.assertEqual(first_word_inside.compoundword, None) # and now is 'Learning'
#         self.assertEqual(second_word_inside.compoundword, None) # and now is 'Learning'
#         self.assertEqual(first_word_inside.show_compoundword, False) # and now is 'Learning'
#         # and good css:
#         firstword_after = self.find(By.XPATH, '//span[@wowordtext="carry"]')
#         secondword_after = self.find(By.XPATH, '//span[@wowordtext="over"]')
#         self.assertEqual(firstword_after.get_attribute('cowostatus'), '0')
#         self.assertEqual(secondword_after.get_attribute('cowostatus'), '0')
#         self.assertEqual(firstword_after.get_attribute('show_compoundword'), 'False')
#         self.assertEqual(firstword_after.get_attribute('iscompoundword'), 'False')
#         self.assertEqual(firstword_after.get_attribute('title'), 'carry\r▶ Unknown [?]')
# 
#     def test_toggling_show_compoundword(self):
#         language_2 = EnglishLanguagesFactory(owner=self.user_1)
#         Settings_currentlang_id.objects.get(owner=self.user_1).stvalue=language_2
#         text2 = TextsFactory(owner=self.user_1, language=language_2, text='''
#         Do you carry the surplus over?''')
#         splitText(text2)
# 
#         self.selenium.get('{}/text_read/{}'.format(self.live_server_url, text2.id))
#         first_word_before = self.find(By.XPATH, '//span[@wowordtext="carry"]')
#         first_word_before.click()
#         self.wait_until(By.CLASS_NAME, 'tooltiptext')
#         self.wait_until(By.XPATH, '//div[@id="bottomright"]/iframe[@id="dictwebpage"]')
#         second_word_before = self.find(By.XPATH, '//span[@wowordtext="over"]')
#         ActionChains(self.selenium).key_down(Keys.CONTROL).click(second_word_before).key_up(Keys.CONTROL).perform()
# 
#         self.wait_until(By.XPATH, '//textarea[@id="id_sentence"][contains(.,"{carry} the surplus {over}")]') 
# 
#         trans_textarea = self.find(By.XPATH, '//textarea[@id="id_translation"]')
#         trans_textarea.send_keys('excédent')
#         self.find(By.XPATH, '//button[@id="submit_word"]').click()
#         self.wait_until(By.XPATH, '//div[@id="topright"][contains(.,"OK: Term saved.")]')
#         # in DB
#         first_word_DB = Words.objects.get( wordtext="carry")
#         second_word_DB = Words.objects.get( wordtext="over")
#         self.assertEqual(first_word_DB.show_compoundword, True) 
#         self.assertEqual(second_word_DB.show_compoundword, True) 
#         
#         # check untoggling 
#         self.find(By.XPATH, '//span[@wowordtext="carry"]').click()
#         self.find(By.XPATH, '//input[@name="show_compoundword_checkbox"]').click()
#         # check the status of both words
#         # in DB:
#         first_word_DB = Words.objects.get( wordtext="carry")
#         second_word_DB = Words.objects.get( wordtext="over")
#         self.assertEqual(first_word_DB.show_compoundword, False) 
#         self.assertEqual(second_word_DB.show_compoundword, False)
#         # in HTML:
#         first_word = self.find(By.XPATH, '//span[@wowordtext="carry"]')
#         second_word = self.find(By.XPATH, '//span[@wowordtext="over"]')
#         self.assertEqual(first_word.get_attribute('show_compoundword'), 'false')
#         self.assertEqual(second_word.get_attribute('show_compoundword'), 'false')
# 
#         # and toggling again 
#         self.find(By.XPATH, '//span[@wowordtext="carry"]').click()
#         self.find(By.XPATH, '//input[@name="show_compoundword_checkbox"]').click()
#         # check the status of both words
#         # in DB:
#         first_word_DB = Words.objects.get( wordtext="carry")
#         second_word_DB = Words.objects.get( wordtext="over")
#         self.assertEqual(first_word_DB.show_compoundword, True) 
#         self.assertEqual(second_word_DB.show_compoundword, True)
#         # in HTML:
#         first_word = self.find(By.XPATH, '//span[@wowordtext="carry"]')
#         second_word = self.find(By.XPATH, '//span[@wowordtext="over"]')
#         self.assertEqual(first_word.get_attribute('show_compoundword'), 'true')
#         self.assertEqual(second_word.get_attribute('show_compoundword'), 'true')