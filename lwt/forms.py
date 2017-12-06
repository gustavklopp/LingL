from django import forms

from django.urls import reverse
from django.utils.translation import ugettext as _, get_language_info
from django.conf.locale import LANG_INFO
from django.db import transaction
# Second party:
import re
import json
# third party
from tags_input import fields as tag_fields, widgets as tag_widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field, Submit, Button, Div, HTML
from allauth.account.forms import SignupForm, LoginForm 
from allauth.account.adapter import get_adapter
# TO CHANGE
from splitjson import fields as json_fields, widgets as json_widgets
# local
from lwt.models import *
from crispy_forms.bootstrap import  FieldWithButtons, FormActions


# class TexttagForm(forms.Form):
#     tags = fields.TagsInputField(
#         models.Texttags.objects.all(),
#         widget=widgets.TagsInputWidget(
#             on_add_tag='updateTag',
#             on_remove_tag='updateTag',
#             on_change_tag='updateTag',
#         ),
# )


class DropdownToggleWidget(forms.TextInput):
    ''' editable dropdown list
        <div class="input-group dropdown">
          <input type="text" class="form-control countrycode dropdown-toggle" value="(+47)">
          <ul class="dropdown-menu">
            <li><a href="#" data-value="+47">Norway (+47)</a></li>
            <li><a href="#" data-value="+1">USA (+1)</a></li>
            <li><a href="#" data-value="+55">Japan (+55)</a></li>
          </ul>
          <span role="button" class="input-group-addon dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="caret"></span></span>
        </div>
    '''
    def __init__(self, data_list, name, *args, **kwargs):
        super(DropdownToggleWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'value': '', 'class':'lang_name dropdown-toggle'})

    def render(self, name, value, attrs=None):
        text_html = super(DropdownToggleWidget, self).render(name, value, attrs=attrs)
        data_list = ''
#         data_list = '<span class="myarrow">'
        data_list += '<ul class="dropdown-menu" id="list__{}">'.format(self._name)
        for item in self._list:
            data_list += '<li><a href="#" data-value="{}">{}</a></li>'.format(item[0], item[1])
        data_list += '</ul><span role="button" class="'
        if not self._list:
            data_list += ' hidden ' # don't dispaly the button to expand the list if no list
        data_list += ' input-group-addon dropdown-toggle" data-toggle="dropdown"'
        data_list += 'aria-haspopup="true" aria-expanded="false"><span class="caret"></span></span>'

        return text_html + data_list
    
    
def make_languagesform(dicturi_list=[]):
    ''' pre-initializing LanguagesForm with datalist for the DropDownToggle widget '''
    class LanguagesForm(forms.ModelForm):
        # load and get the real name for the Fixtures of languages (in lwt/fixtures folder)
        with open('lwt/fixtures/languages_fixtures.json') as lang_json:
            lang_json = lang_json.read()
        languages_fixtures = json.loads(lang_json)
        lang_list = languages_fixtures['_languages']
        name_lang_list = []
        for lang in lang_list:
            if 'django_code' in lang.keys() and lang['django_code'] != "":
                lang_code = lang['django_code']
                name_lang_list.append((lang['code_639_1'], get_language_info(lang_code)['name_translated']))
            else:
                name_lang_list.append((lang['code_639_1'], lang['notlocalized_name']))
        name_lang_list.sort(key=lambda a: a[1])
        # these 3 ones have an editable dropdown input
        name = forms.CharField(required=True, max_length=40, widget=DropdownToggleWidget(name_lang_list, 'name_lang'))  
        dict1uri = forms.CharField(max_length=200, widget=DropdownToggleWidget(dicturi_list, 'dict1uri'))
        dict2uri = forms.CharField(max_length=200, required=False, widget=DropdownToggleWidget(dicturi_list, 'dict2uri'))

        googletranslateuri = forms.CharField(max_length=200, required=False)
        exporttemplate = forms.CharField(widget=forms.Textarea, required=True)
        TEXTSIZE_CHOICES = ((100,100),(150,150),(200,200),(250,250))
        textsize = forms.ChoiceField(choices=TEXTSIZE_CHOICES, widget=forms.Select(), required=True)
        charactersubstitutions = forms.CharField(max_length=500)
        regexpsplitsentences = forms.CharField(max_length=500)
        exceptionssplitsentences = forms.CharField(max_length=500)
        regexpwordcharacters = forms.CharField(max_length=500)
        BOOL_CHOICES = (
            (True, _('Yes')), (False, _('No'))
            )
        removespaces = forms.ChoiceField(choices=BOOL_CHOICES,  widget=forms.Select(), required=True)
        spliteachchar = forms.ChoiceField(choices=BOOL_CHOICES, widget=forms.Select(), required=True)
        righttoleft = forms.ChoiceField(choices=BOOL_CHOICES, widget=forms.Select(), required=True)
        extra_field_key = tag_fields.TagsInputField(Extra_field_key.objects.all(),
                                                    create_missing=True,
                                                    required=False) 

        def __init__(self, *args, **kwargs):
            super(LanguagesForm, self).__init__(*args,**kwargs)
      
            self.helper = FormHelper()
            self.helper.form_class = 'form-horizontal text_detail'
            self.helper.label_class = 'col-md-3'
            self.helper.field_class = 'col-md-6 input-group'
            self.helper.add_input(Submit('save', 'save'))
            self.helper.layout = Layout(
                Field('owner', type="hidden"),
            'name', 'dict1uri', 'dict2uri', 'googletranslateuri', 'exporttemplate', 'textsize',\
             'charactersubstitutions', 'regexpsplitsentences', 'exceptionssplitsentences',\
            'regexpwordcharacters', 'removespaces', 'spliteachchar', 'righttoleft',
            'code_639_1','code_639_2t','code_639_2b','django_code', 'extra_field_key')
            # overriding this because bug when rendering with the error and the dropdowntoglle
            self.helper.field_template = 'custom_bootstrap_field.html'
            # rename the labels for the field:
            self.fields['dict1uri'].label = _('Link to 1st dictionary')
            self.fields['dict2uri'].label = _('Link to 2st dictionary')
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
    language = forms.ModelChoiceField(Languages.objects.all(),empty_label=_("[Choose...]"),
                                      required=True)
    owner = forms.ModelChoiceField(MyUser.objects.all(), required=True)
    title = forms.CharField(max_length=200,required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 60}), required=True)
#                                                         'pattern':'.*\p{L}.*'}))
    annotatedtext = forms.CharField(required=False)
    audiouri = forms.URLField(required=False,max_length=1000)
    sourceuri = forms.URLField(required=False,max_length=200)
    texttags = tag_fields.TagsInputField( Texttags.objects.all(),
                                    create_missing=True,
                                    required=False) 
    
    def __init__(self, *args, **kwargs):
        super(TextsForm, self).__init__(*args,**kwargs)
  
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
            'language', 'title')
        self.helper_edit2 = FormHelper()
        self.helper_edit2.label_class = 'col-md-3'
        self.helper_edit2.field_class = 'col-md-9'
        self.helper_edit2.form_tag = False
        self.helper_edit2.layout = Layout(
            'annotatedtext','audiouri','sourceuri','texttags')
 
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
        self.helper.field_class = 'col-md-6'
        self.helper.layout = Layout(
            FieldWithButtons(
            'uploaded_text', Submit(name='uploaded_text', value=_("Upload your text file"), 
            onclick='$("#uploaded_textform").submit(ajax_uploaded_text());',
#                                                             function(){'+
#                                                                 'console.log("TEST");'+
#                                                                 'ajax_uploaded_text();'+
#                                                                 '});'+
#                     'return false;', 
            css_class='btn-primary'))
        )
        
        
    class Meta:
        model = Uploaded_text
        fields = ['uploaded_text']
        

''' Used by Django-allauth: custom forms '''
class MySignUpForm(SignupForm):
    django_code_list = list(set(LANG_INFO.keys()))
    LANG_CHOICES = [[i, get_language_info(i)['name_translated']] for i in django_code_list]
    LANG_CHOICES.sort(key=lambda a: a[1])
    # remove duplicates ('simplidied Chinese' is in 4 example (with different code)
    LANG_CHOICES_NODUP = []
    I = ''
    for i in LANG_CHOICES:
        if i[1] != I:
            LANG_CHOICES_NODUP.append(i)
        I = i[1]
    origin_lang_code = forms.ChoiceField(choices=LANG_CHOICES_NODUP, required=True)

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
           HTML('<div class="controls col-md-3"><button class="btn btn-info" href="'+ 
                reverse('account_reset_password')+ '">' +_('Forgot Password?')+'</a></div>'),
           HTML('<div class="controls col-md-3"><button class="btn btn-primary" type="submit">'+
                _('Log In')+'</button></div>')
        # NOT WORKING #
#             <div class="controls col-md-3"> <button type="submit"
#     name="login" class="btn btn-primary" id="submit-id-login">Login</button></div>''')
        # END NOT WORKING #
            )
        
        