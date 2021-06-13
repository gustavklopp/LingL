from django.test import TestCase, Client, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
# helper functions
from lwt.views._setting_cookie_db import *
from lwt.views.text import *
from lwt.models import *
from lwt.factories import *
# second-party
import os
import gzip
import io
import tempfile



def add_session_to_request( request):
    """Annotate a request object with a session (RequestFactory doesn't permit Session"""
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    
    
class Test_views(TestCase):
    
    def setUp(self):
        pwd = '12345'
        self.user_1 = UserFactory(password=pwd)
        self.client.login(username=self.user_1.username, password=pwd)
        self.language_1 = LanguagesFactory(owner=self.user_1)
        super(Test_views, self).setUpClass()
 
    def test_only_user_can_see_homepage(self):
        response = self.client.get(reverse('homepage')) 
        self.assertEqual(response.status_code, 200) # access by registered user
        self.client.logout()
        response = self.client.get(reverse('homepage')) 
        self.assertEqual(response.status_code, 302) # access by unregistered user
        
    def test_only_user_with_currentlang_can_see_text_list(self):
        response = self.client.get(reverse('text_list')) 
        self.assertEqual(response['Location'], reverse('homepage')) # trying without cookie

    def test_only_user_with_currentlang_IN_COOKIE_can_see_text_list(self): # and now with a cookie
        session = self.client.session
        session['currentlang_id'] = self.language_1.id
        session.save()
        response = self.client.get(reverse('text_list'))
        self.assertEqual(response.status_code, 200) 

    def test_only_user_with_currentlang_IN_DB_can_see_text_list(self): # and now with database
        Settings_currentlang_idFactory(owner=self.user_1, stvalue=self.language_1.id)
        response = self.client.get(reverse('text_list')) 
        self.assertEqual(response.status_code, 200) 

    def test_user_can_see_his_text(self):
        session = self.client.session
        session['currentlang_id'] = self.language_1.id
        session.save()
        text1 = TextsFactory(owner=self.user_1, language=self.language_1)
        response = self.client.get(reverse('text_list')) 
        self.assertEqual(response.status_code, 200) # access by registered user
        self.assertNotContains(response, 'No texts found.')
        self.assertContains(response, text1.title)
        
    def test_each_user_can_only_see_his_own_text(self):
        text1 = TextsFactory(owner=self.user_1, language=self.language_1)
        
        # create a second user
        pwd = '12345'
        user_2 = UserFactory(password=pwd)
        language_2 = LanguagesFactory(owner=user_2)
        Settings_currentlang_idFactory(owner=user_2, stvalue=language_2.id)
        text2 = TextsFactory(owner=user_2, language=language_2)
        
        session = self.client.session
        session['currentlang_id'] = self.language_1.id
        session.save()
        response = self.client.get(reverse('text_list')) 
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'No texts found.')
        self.assertContains(response, text1.title)
        self.assertNotContains(response, text2.title)

        self.client.logout()
        session = self.client.session
        session['currentlang_id'] = language_2.id
        session.save()

        self.client.login(username=user_2.username, password=pwd)
        response = self.client.get(reverse('text_list')) 
        self.assertEqual(response.status_code, 200) # access by registered user
        self.assertNotContains(response, 'No texts found.')
        self.assertContains(response, text2.title)
        self.assertNotContains(response, text1.title)

    def test_change_currentlang(self):
        Settings_currentlang_idFactory(owner=self.user_1, stvalue=self.language_1.id)
        language_2 = LanguagesFactory(owner=self.user_1)
        response = self.client.get(reverse('text_list'), {'setcurrentlang': str(language_2.id)})
        self.assertEqual(response.status_code, 200) 
        
    def test_language_new_with_no_name(self):
        # trying to create a language with no name:
        response = self.client.post(reverse('language_detail'), {
                   'owner' : self.user_1}) 
        self.assertEqual(response.status_code, 200) 

    def test_empty_database(self):
        for i in range(20):
            TextsFactory(owner=self.user_1, language=self.language_1)
        count = len(Texts.objects.all())
        self.assertEqual(20, count)
        self.client.post(reverse('backuprestore'), {'empty':'empty'})
        count = len(Texts.objects.all())
        self.assertEqual(0, count)

    def test_backup_database(self):
        for i in range(20):
            TextsFactory(owner=self.user_1, language=self.language_1)
        response = self.client.post(reverse('backuprestore'), {'backingup':'backingup'})
        self.assertIn('attachment', response['Content-Disposition'])
        out = io.BytesIO(response.content)
        with gzip.open(out,encoding="utf8", 'r') as f: # uncompress it
            json_text = f.read().decode()
        count = json_text.count('lwt.texts')
        self.assertEqual(20, count)

    def test_restore_database_uncompresseddata(self):
        for i in range(20):
            TextsFactory(owner=self.user_1, language=self.language_1)
        response = self.client.post(reverse('backuprestore'), {'backingup':'backingup'})
        self.assertIn('attachment', response['Content-Disposition'])
        out = io.BytesIO(response.content)
        fp = tempfile.NamedTemporaryFile(suffix='.json')
        with gzip.open(out,encoding="utf8", 'r') as f:
            fp.write(f.read())
        fp.seek(0)
        response = self.client.post(reverse('backuprestore'), {'restore':'restore', 'restore_file':fp})
        fp.close()
        qr_texts = Texts.objects.values().all()
        self.assertNotEqual(len(qr_texts), 0)

    def test_restore_database_compresseddata(self):
        for i in range(20):
            TextsFactory(owner=self.user_1, language=self.language_1)
        response = self.client.post(reverse('backuprestore'), {'backingup':'backingup'})
        self.assertIn('attachment', response['Content-Disposition'])
        out = io.BytesIO(response.content)
        fp = tempfile.NamedTemporaryFile(suffix='.json')
        fp.write(out.getvalue())
        fp.seek(0)
        response = self.client.post(reverse('backuprestore'), {'restore':'restore', 'restore_file':fp})
        fp.close()
        qr_texts = Texts.objects.values().all()
        self.assertNotEqual(len(qr_texts), 0)
        # check that the directory of media has been cleaned out:
        for dirpath, dirnames, files in os.walk(settings.MEDIA_ROOT):
            self.assertFalse(files)


class Helper_func_setting_cookie_db(TestCase): # testing helper function in module _setting_cookie_db

    def setUp(self):
        super(Helper_func_setting_cookie_db, self).setUp()
        self.stkey = 'tags_per_page'
        self.stdft = Settings_tags_per_page._meta.get_field('stdft').get_default()
        self.user_1 = User.objects.create_user(username='user_1', password='12345')
        self.client.login(username='user_1', password='12345')
        factory = RequestFactory()
        self.request = factory.get(reverse('homepage'))
        add_session_to_request(self.request)
        self.request.user = self.user_1

    def tearDown(self):
        super(Helper_func_setting_cookie_db, self).tearDown()

    def test_getter_setting_without_a_cookie_and_nothing_in_database(self):
        # test without a cookie and nothing in database: return the default value (100 here)
        stvar = getter_settings_cookie_else_db(self.stkey, self.request) 
        self.assertEqual(stvar, self.stdft)

    def test_getter_setting_without_a_cookie_but_with_database(self):
        # test without a cookie but with database:
        Settings_tags_per_page.objects.create(owner=self.user_1, stvalue=22)
        stvar = getter_settings_cookie_else_db(self.stkey, self.request) 
        self.assertEqual(stvar, 22)

    def test_getter_setting_with_a_cookie(self):
        # and now with a cookie
        session = self.request.session
        session['tags_per_page'] = 11
        session.save()
        stvar = getter_settings_cookie_else_db(self.stkey, self.request) 
        self.assertEqual(stvar, 11)
        
    def test_setter_setting_change_currentlang(self):
        language_1 = LanguagesFactory(owner=self.user_1)
        Settings_currentlang_idFactory(owner=self.user_1, stvalue=language_1.id)
        language_2 = LanguagesFactory(owner=self.user_1) # change currentlang
        setter_settings_cookie_and_db('setcurrentlang', language_2.id, self.request)
        # check if the cookies has been changed
        session = self.request.session
        self.assertEqual(session['currentlang_id'], language_2.id)
        self.assertEqual(session['currentlang_name'], language_2.name)
        # and the db
        currentlang_id = Settings_currentlang_id.objects.filter(owner=self.request.user).get()
        currentlang_name = Settings_currentlang_name.objects.filter(owner=self.request.user).get()
        self.assertEqual(currentlang_id.stvalue, str(language_2.id))
        self.assertEqual(currentlang_name.stvalue, language_2.name)
        

class Test_views_old_lwt(TestCase):
    fixtures = ['lwt/fixtures/old_lwt.json']
    
    def setUp(self):
        pwd = '12345'
        self.user_1 = User.objects.get(username='oldlwt')
        self.client.login(username=self.user_1.username, password=pwd)
        self.language_1 = Languages.objects.get(name='Italian')
        super(Test_views_old_lwt, self).setUpClass()
 
        
    def test_can_see_text_list(self):
        response = self.client.get(reverse('text_list')) 
        self.assertEqual(response['Location'], reverse('homepage')) # trying without cookie 