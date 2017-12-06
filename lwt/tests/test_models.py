#django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# third party
# from model_mommy import mommy
# from model_mommy.recipe import Recipe, foreign_key
# local
from lwt.factories import *
from lwt.forms import *
from lwt.models import *
from lwt.views._utilities_views import *
from lwt import models
from lwt.insert_old_lwt.insert_old_lwt import *
from django.templatetags.i18n import language


class Test_models(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super(Test_models, cls).setUpClass()


    @classmethod
    def tearDownClass(cls):
        super(Test_models, cls).tearDownClass()
    
    def test_correctdata_in_Texts(self):
        user_1 = UserFactory()
        language_1 = LanguagesFactory(owner=user_1)
        text1 = TextsFactory(owner=user_1, language=language_1)
        data = {
                'language' : language_1.id,
                'title' : 'My title',
                'text' : 'My text',
                'owner': user_1.id
#                 'annotatedtext' : '',
#                 'audiouri': '',
#                 'sourceuri' : '',
#                 'texttags' : ''
                }
        form = TextsForm(data, instance=text1)
        if not form.is_valid():
            print('errors :', form.errors)
        self.assertTrue(form.is_valid())
        
    def test_onlysymbols_in_Texts(self):
        user_1 = UserFactory()
        language_1 = LanguagesFactory(owner=user_1)
        text1 = TextsFactory(owner=user_1, language=language_1)
        data = {
                'language' : language_1.id,
                'title' : 'My title',
                'text' : '124. 569',
                'owner': user_1.id
#                 'annotatedtext' : '',
#                 'audiouri': '',
#                 'sourceuri' : '',
#                 'texttags' : ''
                }
        form = TextsForm(data, instance=text1)
        if not form.is_valid():
            print('errors :', form.errors)
        self.assertFalse(form.is_valid())

        
    def test_splitText_punctuation(self):
        ''' helper function to split the text when creating a new text '''
        user_1 = UserFactory()
        language_1 = LanguagesFactory(owner=user_1)
        text1 = TextsFactory(owner=user_1, language=language_1, text='This, is a text. Indeed it\'s a text - or not?')
        splitText(text1)
        sentences = Sentences.objects.filter(owner=user_1).all()
        self.assertEqual(sentences[0].sentencetext, 'This, is a text.')
        self.assertEqual(sentences[1].sentencetext, ' Indeed it\'s a text - or not?')
        wordsdict = Words.objects.filter(owner=user_1).values('id','wordtext','isnotword','order')
        words = Words.objects.filter(owner=user_1).all()
        for i in wordsdict:
            print(i)
        self.assertEqual(words[1].wordtext, ', ')
        self.assertEqual(words[1].isnotword, True)

    def test_splitText_not_ending_with_punctuation(self):
        ''' helper function to split the text when creating a new text '''
        user_1 = UserFactory()
        language_1 = LanguagesFactory(owner=user_1)
        text1 = TextsFactory(owner=user_1, language=language_1, 
                             text='Mitleiden hängen bleiben: und gälte es höheren Menschen, in deren')
        splitText(text1)
        sentences = Sentences.objects.filter(owner=user_1).all()
        self.assertEqual(sentences[1].sentencetext, ' und gälte es höheren Menschen, in deren')
        wordsdict = Words.objects.filter(owner=user_1).values('id','wordtext','isnotword','order')
        words = Words.objects.filter(owner=user_1).filter(isnotword=False).all()
        self.assertEqual(len(words), 10)
    
    def test_splitText_not_ending_with_punctuation2(self):
        ''' helper function to split the text when creating a new text '''
        user_1 = UserFactory()
        language_1 = LanguagesFactory(owner=user_1)
        text1 = TextsFactory(owner=user_1, language=language_1, 
                             text='Wiederhall der Öde, Etwas von dem Flüstertone und dem scheuen')
        splitText(text1)
        sentences = Sentences.objects.filter(owner=user_1).all()
        self.assertEqual(sentences[0].sentencetext, 'Wiederhall der Öde, Etwas von dem Flüstertone und dem scheuen')
        wordsdict = Words.objects.filter(owner=user_1).values('id','wordtext','isnotword','order')
        words = Words.objects.filter(owner=user_1).filter(isnotword=False).all()
        self.assertEqual(len(words), 10)
        
    def test_splitText_chinese_single_sentence(self):
        ''' helper function to split the text when creating a new text '''
        user_1 = UserFactory()
        language_1 = ChineseLanguagesFactory(owner=user_1)
        text1 = TextsFactory(owner=user_1, language = language_1,
                             text= ' 大家好，我是Jenny.')
        splitText(text1)
        sentences = Sentences.objects.filter(owner=user_1).all()
        wordsdict = Words.objects.filter(owner=user_1).values('id','wordtext','isnotword','order','sentence_id')
        words = Words.objects.filter(owner=user_1).filter(isnotword=False).all()
        for i in wordsdict:
            print(i)
        self.assertEqual(sentences[0].sentencetext, ' 大家好，我是Jenny.')
        self.assertEqual(len(words), 5)

    def test_splitText_chinese_several_sentences(self):
        ''' helper function to split the text when creating a new text '''
        user_1 = UserFactory()
        language_1 = ChineseLanguagesFactory(owner=user_1)
        text1 = TextsFactory(owner=user_1, language = language_1,
                     text='''
介绍\n\n 大家好，我是Jenny. 今天，我和Ken 为大家准备了。一个中级课\n　程.在以后的时间里，我们会为大家准备更多的中级课程。\n\n　重点句式\n\n\n1． 老师，早上好。
                        '''
                        )
        splitText(text1)
        sentences = Sentences.objects.filter(owner=user_1).all()
        wordsdict = Words.objects.filter(owner=user_1).values('id','wordtext','isnotword','order','sentence_id')
        words = Words.objects.filter(owner=user_1).filter(isnotword=False).all()
        for i in wordsdict:
            print(i)
        self.assertEqual(sentences[4].sentencetext, ' 今天，我和Ken 为大家准备了。')
        self.assertEqual(len(sentences), 15)
#                         介绍\n\n　大家好，我是Jenny. 今天，我和Ken 为大家准备了一个中级课\n　程.在以后的时间里，我们会为大家准备更多的中级课程。\n\n　重点句式\n\n\n1． 老师，早上好。\n\n2． 同学们，早上好。\n\n3． 今天，我们要学什么呢？\n\n4． 今天，我们要学怎样学习中级中文。\n\n5． 老师，我怎么样能提高我的中文呢？\n \n　现在你已经是中级学生了，你需要两样东西。第一是投入，就是\n　学习资料。它必须是有意义的，难度适中的。如果太难，你不会\n　懂；如果太简单，你不会学到新的东西。还有一个就是付出，也\n　就是练习，比如口语练习。

    def test_splitText_chinese_several_sentences2(self):
        ''' helper function to split the text when creating a new text '''
        user_1 = UserFactory()
        language_1 = ChineseLanguagesFactory(owner=user_1)
        text1 = TextsFactory(owner=user_1, language = language_1,
text='介绍\n\n\u3000大家好，我是Jenny. 今天，我和Ken 为大家准备了一个中级课\n\u3000程.在以后的时间里，我们会为大家准备更多的中级课程。\n\n\u3000重点句式\n\n\n1． 老师，早上好。\n\n2． 同学们，早上好。\n\n3． 今天，我们要学什么呢？\n\n4． 今天，我们要学怎样学习中级中文。\n\n5． 老师，我怎么样能提高我的中文呢？\n \n\u3000现在你已经是中级学生了，你需要两样东西。第一是投入，就是\n\u3000学习资料。它必须是有意义的，难度适中的。如果太难，你不会\n\u3000懂；如果太简单，你不会学到新的东西。还有一个就是付出，也\n\u3000就是练习，比如口语练习。'
                        )
        splitText(text1)
        sentences = Sentences.objects.filter(owner=user_1).all()
        wordsdict = Words.objects.filter(owner=user_1).values('id','wordtext','isnotword','order','sentence_id')
        words = Words.objects.filter(owner=user_1).filter(isnotword=False).all()
        for i in wordsdict:
            print(i)
        self.assertEqual(sentences[3].sentencetext, ' 今天，我和Ken 为大家准备了一个中级课')
        self.assertEqual(len(sentences), 34)

    def test_splitText_hebrew(self):
        # TODO: Hebrew
        ''' helper function to split the text when creating a new text '''
        user_1 = UserFactory()
        language_1 = HebrewLanguagesFactory(owner=user_1)
        text1 = TextsFactory(owner=user_1, language = language_1,
                text='בוקר טוב\nאחר צהריים טובים\nערב טוב\nלילה טוב\nלהתראות')
        splitText(text1)
        sentences = Sentences.objects.filter(owner=user_1).all()
        wordsdict = Words.objects.filter(owner=user_1).values('id','wordtext','isnotword','order','sentence_id')
        words = Words.objects.filter(owner=user_1).filter(isnotword=False).all()
        for i in wordsdict:
            print(i)
        self.assertEqual(sentences[8].sentencetext, 'טוב בוקר')
        self.assertEqual(len(sentences), 9)

    def test_insert_old_lwt(self):
        '''using helper function to insert_into_db'''
        user_1 = UserFactory(username='oldlwt')
        Settings_currentlang_idFactory(owner=user_1, stvalue=1)
        insert_into_db(models, user_1) 
        qr_languages = Languages.objects.filter(id=1).values().all()
        qr_texts = Texts.objects.values().all()
        qr_words = Words.objects.filter(language_id=1).values().all()
        qr_learningwords = Words.objects.filter(language_id=1, status=1).values().all()
#         qr_words = Words.objects.values().all()
        for i in qr_learningwords:
            print(i)
        self.assertNotEqual(len(qr_languages), 0)
        self.assertNotEqual(len(qr_texts), 0)
        self.assertNotEqual(len(qr_words), 0)
        self.assertNotEqual(len(qr_learningwords), 0)
        from django.core.serializers import serialize

        qs_0 = User.objects.all()
        qs_1 = Languages.objects.all()
        qs_2 = Texttags.objects.all()
        qs_3 = Texts.objects.all()
        qs_4 = Sentences.objects.all()
        qs_5 = Wordtags.objects.all()
        qs_6 = Wordtags.objects.all()
        qs_7 = Grouper_of_same_words.objects.all()
        qs_8 = Words.objects.all()
# 
#         qs_9 = Settings_text_h_frameheight_no_audio.objects.all()
#         qs_10 = Settings_text_h_frameheight_with_audio.objects.all()
#         qs_11 = Settings_text_l_framewidth_percent.objects.all()
#         qs_12 = Settings_text_r_frameheight_percent.objects.all()
#         qs_13 = Settings_test_h_frameheight.objects.all()
#         qs_14 = Settings_test_l_framewidth_percent.objects.all()
#         qs_15 = Settings_test_r_frameheight_percent.objects.all()
#         qs_16 = Settings_test_main_frame_waiting_time.objects.all()
#         qs_17 = Settings_test_edit_frame_waiting_time.objects.all()
#         qs_18 = Settings_test_sentence_count.objects.all()
#         qs_19 = Settings_term_sentence_count.objects.all()
#         qs_20 = Settings_archivedtexts_per_page.objects.all()
#         qs_21 = Settings_texts_per_page.objects.all()
#         qs_22 = Settings_terms_per_page.objects.all()
#         qs_23 = Settings_tags_per_page.objects.all()
#         qs_24 = Settings_show_all_words.objects.all()
#         qs_25 = Settings_show_text_word_counts.objects.all()
#         qs_26 = Settings_text_visit_statuses_via_key.objects.all()
#         qs_27 = Settings_term_translation_delimiters.objects.all()
#         qs_28 = Settings_mobile_display_mode.objects.all()
#         qs_29 = Settings_similar_terms_count.objects.all()
#         # current settings
#         qs_30 = Settings_currentlang_name.objects.all()
        qs_31 = Settings_currentlang_id.objects.all()
#         qs_32 = Settings_currenttext_id.objects.all()
#         qs_33 = Settings_currenttextpage.objects.all()
#         qs_34 = Settings_currenttextquery.objects.all()
#         qs_35 = Settings_currenttextsort.objects.all()
#         qs_36 = Settings_currentwordpage.objects.all()
#         qs_37 = Settings_currentwordquery.objects.all()
#         qs_38 = Settings_currentwordstatus.objects.all()
#         qs_39 = Settings_currentwordsort.objects.all()
#         qs_40 = Settings_currentwordtag1.objects.all()
#         qs_41 = Settings_currentwordtag2.objects.all()
#         qs_42 = Settings_currentwordtag12.objects.all()
#         qs_43 = Settings_currentarchivepage.objects.all()
#         qs_44 = Settings_currentarchivequery.objects.all()
#         qs_45 = Settings_currentarchivetexttag1.objects.all()
#         qs_46 = Settings_currentarchivetexttag2.objects.all()
#         qs_47 = Settings_currentarchivetexttag12.objects.all()
        
        all_qs = []
        for i in range(0,9):
            all_qs += eval('qs_' + str(i))
        all_qs += qs_33

        fixture = serialize('json', all_qs)
        with open('lwt/fixtures/old_lwt.json', 'w') as f:
            f.write(fixture)


        