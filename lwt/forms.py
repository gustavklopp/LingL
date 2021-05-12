from django import forms

from django.urls import reverse
from django.utils.translation import ugettext as _, get_language_info
from django.conf.global_settings import LANGUAGES
from django.conf import settings
from django.db import transaction
# Second party:
import os
import re
import json
# third party
from tags_input import fields as tag_fields, widgets as tag_widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field, Submit, Button, Div, HTML     
from crispy_forms.bootstrap import  FieldWithButtons, FormActions, StrictButton,\
    AppendedText
from allauth.account.forms import SignupForm, LoginForm 
from allauth.account.adapter import get_adapter
# TO CHANGE
from splitjson import fields as json_fields, widgets as json_widgets
# local
from lwt.models import Languages, Texts, Extra_field_key, MyUser, Texttags, Words, Wordtags, Restore, Uploaded_text


# class TexttagForm(forms.Form):
#     tags = fields.TagsInputField(
#         models.Texttags.objects.all(),
#         widget=widgets.TagsInputWidget(
#             on_add_tag='updateTag',
#             on_remove_tag='updateTag',
#             on_change_tag='updateTag',
#         ),
# )


''' appended button to input with dropdown list
   look here to know Bootstrap does the style: https://getbootstrap.com/docs/4.0/components/input-group/#buttons-with-dropdowns
   <div class="input-group-append">
    <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></button>
    <div class="dropdown-menu">
      <a class="dropdown-item" href="#">Action</a>
      ... 
    </div>
  </div>
'''
class DropdownToggleWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(DropdownToggleWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'value': '', 'class':'lang_name dropdown-toggle'})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(DropdownToggleWidget, self).render(name, value, attrs=attrs)
        data_list = ''
#         data_list = '<span class="myarrow">'
        data_list += '<div class="'
        if not self._list:
            data_list += ' hidden ' # don't display the button to expand the list if no list
        data_list += ' input-group-append" id="input-group-append_list__{}">'.format(self._name)
        data_list += '<button class="btn btn-outline-secondary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></button>'
        data_list += '<div class="dropdown-menu" id="list__{}">'.format(self._name)
        for item in self._list:
            data_list += '<a class="dropdown-item" href="#" data-value="{}">{}</a>'.format(item[0], item[1])
        data_list += '</div></div>'

        return text_html + data_list
    
''' pre-initializing LanguagesForm with datalist for the DropDownToggle widget '''
def make_languagesform(user_id, dicturi_list=[]):
    class LanguagesForm(forms.ModelForm):

        lang_list = Languages.objects.filter(owner_id=1)
        name_lang_list = []
        for lang in lang_list:
            lang_code = lang.django_code
            name_lang_list.append((lang.code_639_1, 
                                   get_language_info(lang_code)['name_translated']))
        name_lang_list.sort(key=lambda a: a[1])
        # these 3 ones have an editable dropdown input
        name = forms.CharField(required=True, max_length=40, 
                               widget=DropdownToggleWidget(name_lang_list, 'name_lang',
                                       attrs={'title':_('name of the language'),
                                              'placeholder': _('You can choose predefined languages by clicking on the arrow on the right -->')}))  
        dict1uri = forms.CharField(required=True, max_length=200, 
                                   widget=DropdownToggleWidget(dicturi_list, 'dict1uri',
                                       attrs={'title':_('the dictionary which will open when you click on a word')}
                                                               ))
        dict2uri = forms.CharField(required=True, max_length=200,  
                                   widget=DropdownToggleWidget(dicturi_list, 'dict2uri',
                                       attrs={'title':_('another dictionary which will open when you click on a word')}
                                                               ))
        googletranslateuri = forms.CharField(required=True, max_length=200, 
                                       widget=forms.TextInput(attrs={'title':_('link to Google translate')}
                                                               ))
        exporttemplate = forms.CharField(required=True,
                                widget=forms.Textarea(
                                       attrs={'title':_('Template to create Anki cards. See https://docs.ankiweb.net/#/templates/fields to have info about the fields used')}
                                                               ))
        TEXTSIZE_CHOICES = ((100,100),(150,150),(200,200),(250,250))
        textsize = forms.ChoiceField(choices=TEXTSIZE_CHOICES, required=True,
                                     widget=forms.Select(
                                       attrs={'title':_('Size of the text')}
                                         ))
        charactersubstitutions = forms.CharField(max_length=500,
                                   widget=forms.TextInput(attrs={'title':_('Some languages have special punctuation marks. Convert them to your usual punctuation mark for you (e.g: the 、in Japanese')}
                                     ))
        regexpsplitsentences = forms.CharField(max_length=500,
                                   widget=forms.TextInput(attrs={'title':_('What is the punctuation mark used to signal the end of sentence in this anguage?')}
                                     ))
        exceptionssplitsentences = forms.CharField(max_length=500,
                                   widget=forms.TextInput(attrs={'title':_('Sometimes, the punctuation mark used to signal the end of line is also used to signal other things which are NOT end of sentence. For example: "Mr.Smith" for name in English')}
                                                   ))
        regexpwordcharacters = forms.CharField(max_length=500,
                                   widget=forms.TextInput(attrs={'title':_('Which letters are components of this language?')}
                                                   ))
        BOOL_CHOICES = (
            (True, _('Yes')), (False, _('No'))
            )
        removespaces = forms.ChoiceField(choices=BOOL_CHOICES,
                                         required=True,
                                          widget=forms.Select(attrs={'title':_('E.g: in Japanese and Chinese, words are NOT separated by space')}
                                              ))
        spliteachchar = forms.ChoiceField(choices=BOOL_CHOICES,
                                          required=True,
                                          widget=forms.Select(attrs={'title':_('E.g: in Japanese and Chinese, words are mostly composed of one character')}
                                              ))
        has_romanization = forms.ChoiceField(choices=BOOL_CHOICES,
                                          required=True,
                                          widget=forms.Select(attrs={'title':_('E.g: romaji in Japanese and pinyin in Chinese are used to write words in latin letters')}
                                              ))
        righttoleft = forms.ChoiceField(choices=BOOL_CHOICES,
                                        required=True,
                                          widget=forms.Select(attrs={'title':_('E.g: Arabic is written from right to left')}
                                              ))
        extra_field_key = tag_fields.TagsInputField(Extra_field_key.objects.all(),
                                                    create_missing=True,
                                                    required=False
                                              )

        def __init__(self, *args, **kwargs):
            super(LanguagesForm, self).__init__(*args,**kwargs)
      
            self.helper = FormHelper()
            self.helper.form_class = 'form-horizontal text_detail'
            self.helper.label_class = 'col-md-3'
            self.helper.field_class = 'col-md-6 input-group'
            self.helper.add_input(Submit('save', 'save'))
            self.helper.layout = Layout(
                Field('owner', type="hidden"),
                Field('dicturi', type="hidden"),
            'name', 'dict1uri', 'dict2uri', 'googletranslateuri', 'exporttemplate', 'textsize',\
             'charactersubstitutions', 'regexpsplitsentences', 'exceptionssplitsentences',\
            'regexpwordcharacters', 'removespaces', 'spliteachchar', 'has_romanization', 'righttoleft',
            'code_639_1','code_639_2t','code_639_2b','django_code', 'extra_field_key')
            # overriding this because bug when rendering with the error and the dropdowntoglle
#             self.helper.field_template = 'custom_bootstrap_field.html'
            # rename the labels for the field:
            self.fields['dict1uri'].label = _('Link to 1st dictionary')+\
                ' <a href="'+reverse('helppage')+'#dicturi" class="text-muted">['+ _('How to create your own dictionary link?')+']</a>'
            self.fields['dict2uri'].label = _('Link to 2st dictionary')+\
                ' <a href="'+reverse('helppage')+'#dicturi" class="text-muted">['+ _('How to create your own dictionary link?')+']</a>'
            self.fields['googletranslateuri'].label = _('Link to Google translate')
            self.fields['exporttemplate'].label = _('template to export to Anki')
            self.fields['textsize'].label = _('Display size of the characters')
            self.fields['charactersubstitutions'].label = _('Characters which must be converted to')
            self.fields['regexpsplitsentences'].label = _('Characters considered as End of line')
            self.fields['exceptionssplitsentences'].label = _('Group of characters which must NOT be considered as End of Line')
            self.fields['regexpwordcharacters'].label = _('Range of possible characters')
            self.fields['removespaces'].label = _('Are words separated by spaces?')
            self.fields['spliteachchar'].label = _('Do most words composed of only one character?')
            self.fields['righttoleft'].label = _('Is it written from Right to Left?')
            self.fields['has_romanization'].label = _('Possible romanization?')
            self.fields['code_639_1'].label = _('the language code in ISO-639-1 format')
            self.fields['code_639_2t'].label = _('the language code in ISO-639-2t format')
            self.fields['code_639_2b'].label = _('the language code in ISO-639-2b format')
            self.fields['django_code'].label = _('the language code defined in Django docs')
            self.fields['extra_field_key'].label = _('Add additional field(s) that you\'ll need')

        class Meta:
            model = Languages
            fields = '__all__'
            widget= {
                'extra_field_key': tag_widgets.TagsInputWidget, 
            }

    return LanguagesForm


class TextsForm(forms.ModelForm):
#     id = forms.IntegerField()
    language = forms.ModelChoiceField(queryset=None, required=True)
    owner = forms.ModelChoiceField(MyUser.objects.all(), required=True)
    lastopentime = forms.DateTimeField(required=False)
    title = forms.CharField(max_length=200,required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 60}), required=True)
#                                                         'pattern':'.*\p{L}.*'}))
    annotatedtext = forms.CharField(required=False)
    audiouri = forms.URLField(required=False,max_length=1000)
    sourceuri = forms.URLField(required=False,max_length=200)
    texttags = tag_fields.TagsInputField( Texttags.objects.all(),
                                    create_missing=True,
                                    required=False) 
    
    def __init__(self, user, *args, **kwargs):
        super(TextsForm, self).__init__(*args,**kwargs)
  
        # the dropdown menu for Languages only shows the languages owned by User
        self.fields['language'].queryset = Languages.objects.all().filter(owner=user)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal text_detail'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
#         self.helper.add_input(Button(_('Cancel'), css_class='btn',
#                                       onclick="{resetDirty(); location.href='{% url 'text_list' %}?page=1';}"))
#         self.helper.add_input(Button(_('Save and Open'), css_class='btn'))
#         self.helper.add_input(Submit('Save', 'save'))
        self.helper.add_input(Submit('save', 'save'))
        self.helper.layout = Layout(
            Field('owner', type="hidden"),
            'language', 'title','text','annotatedtext','audiouri','sourceuri','texttags') # to automatically put request.user in the database

        # for editing the text
        self.helper_edit1 = FormHelper()
        self.helper_edit1.label_class = 'col-md-3'
        self.helper_edit1.field_class = 'col-md-9'
        self.helper_edit1.form_tag = False
        self.helper_edit1.layout = Layout(
            Field('owner', type="hidden"),
            Field('id', type="hidden"),
            'language', 'title')
        self.helper_edit2 = FormHelper()
        self.helper_edit2.label_class = 'col-md-3'
        self.helper_edit2.field_class = 'col-md-9'
        self.helper_edit2.form_tag = False
        self.helper_edit2.layout = Layout(
            Field('text', type="hidden"),
            Field('lastopentime', type="hidden"),
            'annotatedtext','audiouri','sourceuri','texttags')
        self.helper_edit2.add_input(Submit('save', 'save'))
 
#         if hasattr(self.Meta, 'fields'): delattr(self.Meta, 'fields')

    def clean(self):
        super(TextsForm, self).clean()
        data = self.cleaned_data
        if re.search(r'^[-!$%^&*()_+|~=`{}\[\]:";\'<>?,.\/0-9 ]*$', data['text']):
            message = _('Text should contain characters, not only symbols')
            self.add_error('text', forms.ValidationError(message))
        return data
 
    class Meta:
        model = Texts
        fields = '__all__'
        widget= {
            'texttags': tag_widgets.TagsInputWidget, # getting the tags fo the texts (using Django tagsinput app)
        }
    

class WordsForm(forms.ModelForm):
    status = forms.IntegerField()  
    translation = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    romanization = forms.CharField( max_length=100, required=False)  
    wordtags = tag_fields.TagsInputField( Wordtags.objects.all(),
                                    create_missing=True,
                                    required=False)
    # TO CHANGE
    extra_field = json_fields.SplitJSONField(required=False)

    def __init__(self, *args, **kwargs):
        super(WordsForm, self).__init__(*args,**kwargs)
  
        self.helper = FormHelper()
#         self.helper.label_class = 'col-md-3'
#         self.helper.field_class = 'col-md-9'
#         self.helper.add_input(Button(_('Cancel'), css_class='btn',
#                                       onclick="{resetDirty(); location.href='{% url 'text_list' %}?page=1';}"))
#         self.helper.add_input(Button(_('Save and Open'), css_class='btn'))
#         self.helper.add_input(Submit('Save', 'save'))
        self.helper.add_input(Submit('save', 'save'))
        # rename the labels for the field:
        self.fields['extra_field'].label = _('Extra field') + \
            ' <a href="' + reverse('language_detail') + '?edit=' + \
            str(kwargs['instance'].language.id) + '#extra_field'\
            '">' + _('(manage extra fields)') + '</a>'


    class Meta:
        model = Words
        fields = ('translation','romanization','status','wordtags', 'extra_field')
        widget= {
            'wordtags': tag_widgets.TagsInputWidget, # getting the tags fo the texts (using Django tagsinput app)
            # TO CHANGE
            'extra_field': json_widgets.SplitJSONWidget({'class': 'special', 'size': '40'}, debug=True)
        }


''' Uploading files '''
class RestoreForm(forms.ModelForm):
#     restore_file = forms.FileField()
#     restore_oldlwt_file = forms.FileField()
    
    class Meta:
        model = Restore
        fields = ['restore_file_name', 'restore_file', 'import_oldlwt']
        

class Uploaded_textForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(Uploaded_textForm, self).__init__(*args,**kwargs)
  
        self.helper = FormHelper()
#         self.helper.form_action = reverse('uploaded_text')
        self.helper.form_onsubmit = ''
        self.helper.form_id = 'uploaded_textform'
        self.helper.form_class = 'form-horizontal text_detail'
        self.helper.label_class = 'col-md-3'
#         self.helper.field_class = 'col-md-6'
#         self.helper.layout = Layout(
#             FieldWithButtons(
#             'uploaded_text', Submit(name='uploaded_text', value=_("Upload your text file"), 
#             onclick='$("#uploaded_textform").submit(ajax_uploaded_text());',
# #                                                             function(){'+
# #                                                                 'console.log("TEST");'+
# #                                                                 'ajax_uploaded_text();'+
# #                                                                 '});'+
# #                     'return false;', 
#             css_class='btn-primary'))
#         )
# <div class="input-group mb-3">
#   <div class="custom-file">
#     <input type="file" class="custom-file-input" id="inputGroupFile02">
#     <label class="custom-file-label" for="inputGroupFile02">Choose file</label>
#   </div>
#   <div class="input-group-append">
#     <span class="input-group-text" id="">Upload</span>
#   </div>
# </div>
#         self.helper.layout = Layout(
#             AppendedText('uploaded_text', 'text'
#                          , StrictButton(
#                                 _("Upload your text file"), 
#                                 css_class="btn-primary", 
#                                 onclick='$("#uploaded_textform").submit(ajax_uploaded_text());')
#                 )
#         )
#         self.helper.layout = Layout(
#            Div(HTML('''
#                <div class="custom-file"> 
#                  <input type="file" class="custom-file-input" id="id_uploaded_text">
#                  <label class="custom-file-label" for="id_uploaded_text">{}</label>
#                </div>
#                 <div class="input-group-append">
#                   <span name='uploaded_text' class="input-group-text" 
#                    onclick='$("#uploaded_textform").submit(ajax_uploaded_text());'>{}</span>
#                 </div>'''.format(_('Choose text file'), _('Upload it'))), 
#               css_class="input-group col-md-6 mb-3")  
#            )
        
    class Meta:
        model = Uploaded_text
        fields = ['uploaded_text']
        

''' Used by Django-allauth: custom forms '''
class MySignUpForm(SignupForm):
    try: # Bug? It triggers an error when doing ./manage.py migrate
        # LANG_CHOICES: <class 'list'>: [('zh-cn', 'Chinese'), ('en', 'English'),....
        # displaying the language I know. we need to localized it, and sort it (because by default,
        #.. they are sorted by the lang code, which is not what is displayed to the User
        LOCALIZED_LANGUAGES = [(i[0], get_language_info(i[0])['name_translated']) for i in LANGUAGES]
        LOCALIZED_LANGUAGES.sort(key=lambda tup: tup[1])
        origin_lang_code = forms.ChoiceField(choices=LOCALIZED_LANGUAGES, required=True) # the language I know

        # displaying the language I want to learn:
        # we'll put in database the id and the name (and also in cookie): see in Models.UserAccountAdapter
        languages_list = list(Languages.objects.filter(owner_id=1).values_list('id', 'name').order_by('name'))
        LEARNING_LANG_CHOICES = [(id, _(name)) for id, name in languages_list]
        # LEARNING_LANG_CHOICES has type like: <class 'list'>: 
        #              [('zh-cn+Chinese', localized('Chinese')), ('en+English', localized('English')),....
        AdminUser_learning_lang_id = forms.ChoiceField(choices=LEARNING_LANG_CHOICES, required=True) # the language I want to learn
    except:
        pass

    def __init__(self, *args, **kwargs):
        super(MySignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'signup_form'
        self.helper.form_class = 'signup'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('account_signup')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-3'
        self.fields['origin_lang_code'].label = _('I know')
        self.fields['AdminUser_learning_lang_id'].label = _('I want to learn')
        self.helper.add_input(Submit('signup', _('Sign Up'), css_class='btn btn-primary'))


class MyLogInForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(MyLogInForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'login_form'
        self.helper.form_class = 'login'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('account_login')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-3'
        self.helper.layout = Layout(
           Field('login', 'password'),
            HTML('<div class="row"><div class="col-md-3"></div><div class="col-md-3"><a href="'+ 
                 reverse('account_reset_password')+ '">' +_('Forgot Password?')+'</a></div></div>'),
#            HTML('<div class="controls col-md-3"><button class="btn btn-info" href="'+ 
#                 reverse('account_reset_password')+ '">' +_('Forgot Password?')+'</a></div>'),
           HTML('<div class="controls col-md-3"><button class="btn btn-primary" type="submit">'+
                _('Log In')+'</button></div>')
        # NOT WORKING #
#             <div class="controls col-md-3"> <button type="submit"
#     name="login" class="btn btn-primary" id="submit-id-login">Login</button></div>''')
        # END NOT WORKING #
            )
        
        