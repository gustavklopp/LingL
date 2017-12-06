# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import Client
# second party
import time
import random

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# local
from lwt.factories import *
from lwt.views._utilities_views import *
from selenium.webdriver.common import desired_capabilities


class Base(StaticLiveServerTestCase):

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super(Base, cls).tearDownClass()

    @classmethod
    def find(cls, findhow, findwhere): # wait until and find
        cls.wait_until(findhow, findwhere)
        return cls.selenium.find_element(findhow, findwhere)

    @classmethod
    def finds(cls, findhow, findwhere): # wait until and find
        cls.wait_until(findhow, findwhere)
        return cls.selenium.find_elements(findhow, findwhere)

    @classmethod
    def wait_until(cls, findhow, findwhere):
        WebDriverWait(cls.selenium, 20).until(
            EC.presence_of_element_located((findhow,findwhere))
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
        cls.user_1 = UserFactory(password=cls.pwd)
        super(BasePage_loggedin, cls).setUpClass()

        cls.selenium = WebDriver()
        cls.client = Client()
        cls.client.login(username=cls.user_1.username, password=cls.pwd)
        cookie = cls.client.cookies['sessionid']
        cls.selenium.get('{}'.format(cls.live_server_url))
        cls.selenium.add_cookie({'name':'sessionid', 'value': cookie.value, 'secure':False, 'path':'/'})
        cls.selenium.refresh()
        cls.selenium.get('{}'.format(cls.live_server_url))
                

class Language_detail(BasePage_loggedin):

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
        

    

class Text_detail(BasePage):

    @classmethod
    def setUpClass(cls):
        super(Text_detail, cls).setUpClass()
        cls.language_1 = GermanLanguagesFactory(owner=cls.user_1)
        Settings_currentlang_idFactory(owner=cls.user_1, stvalue=cls.language_1.id)
        cls.selenium.get('{}/accounts/login/'.format(cls.live_server_url))
        cls.selenium.implicitly_wait(10)
        login = cls.selenium.find_element_by_name('login')
        login.send_keys(cls.user_1.username)
        pw = cls.selenium.find_element_by_name('password')
        pw.send_keys(cls.pwd)
        cls.selenium.find_element_by_class_name('primaryAction').click()

    def test_create_a_new_text(self):  
        self.selenium.get('{}/text_detail/new/0/'.format(self.live_server_url))
        select = Select(self.find(By.NAME,'language'))
        select.select_by_visible_text('German')
        title = self.find(By.NAME, 'title')
        title.send_keys('An Example of Title')
        text = self.find(By.NAME,'text')
        text.send_keys('This is the content of this text.')
        save = self.find(By.NAME, 'save')
        save.click()
        self.selenium.get('{}/text_list/'.format(self.live_server_url))

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


class Selenium_old_lwt(StaticLiveServerTestCase):  
    
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
