import six

from django.conf import settings
from django import forms
from django.template.loader import render_to_string
from django import urls
from django.contrib.admin import widgets

try:  
    from collections import OrderedDict
except ImportError: 
    from django.utils.datastructures import SortedDict as OrderedDict


class TagsInputWidgetBase(forms.SelectMultiple):
    ''' the widget for the field (the way the Field will be rendered): it's a selectmultiple HTML.
    TagsInputWidget is the derived clas (it adds a class Media) '''

    def __init__(self, on_add_tag=None, on_remove_tag=None, on_change_tag=None, *args, **kwargs):
        self.on_add_tag = on_add_tag
        self.on_remove_tag = on_remove_tag
        self.on_change_tag = on_change_tag
        forms.SelectMultiple.__init__(self, *args, **kwargs)
        
    # build-in base widget functions:

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs): 
        '''Compatibility function for the behavior changes in Django 1.11+
        return the dictionary of the attributes '''
        attrs = dict(base_attrs or {}, **kwargs) # What is base_attrs?
        if extra_attrs:  # Put some extra attributes in the dict attrs if provided
            attrs.update(extra_attrs)
        return attrs

    def render(self, name, value, attrs=None, renderer=None, choices=()):
        ''' create finally the HTML. it uses the template HTML:tags_input_widget.html '''
        context = self.build_attrs(attrs, name=name) # create the dict of attribute (the last one is the name)
        context['on_add_tag'] = self.on_add_tag # put additional tags on_add_tag, on_remove, on_change
        context['on_remove_tag'] = self.on_remove_tag
        context['on_change_tag'] = self.on_change_tag

        context['STATIC_URL'] = settings.STATIC_URL
        context['mapping'] = self.mapping # self.mapping is in fact created by the TagsInputField:
                                        # self.widget.mapping = self.get_mapping()
        context['autocomplete_url'] = urls.reverse('tags_input:autocomplete',
                                                            kwargs=dict(app=self.mapping['app'],
                                                                        model=self.mapping['model'],
                                                                        fields='-'.join(self.mapping['fields']),),)
        if value:
            fields = self.mapping['fields']
            join_func = self.mapping['join_func']

            ids = []
            for v in value:
                if isinstance(v, six.integer_types):
                    ids.append(v)

            values_map = OrderedDict(map(join_func, 
                                         self.mapping['queryset'].filter(pk__in=ids).values('pk', *fields).order_by('pk')))
            values = []
            for v in value:
                if isinstance(v, six.integer_types):
                    values.append(values_map[v])
                else:
                    values.append(v)
            context['values'] = ', '.join(values)
        return render_to_string('tags_input_widget.html', context)

    def value_from_datadict(self, data, files, name):
        ''' return a dict of the tags 
data is of the type: <QueryDict: 
{'csrfmiddlewaretoken': ['H...3K'], 'wotext': ['how'], 'wotranslation': ['comment'], 'wordtags': ['thatthing thisthing'], 'woromanization': [''], 'wosentence': ['This is {how} it happened in fact.'], 'wostatus': ['1']}>
name is = 'wordtags' for ex. '''
        tags = data.get(name, '').split(' ') # the tags are separated by a space ' ': ['thatthing', 'thisthing']
        incomplete = data.get(name + '_incomplete', '') # don't know what it is
        if incomplete != data.get(name + '_default'):
            tags += incomplete.split(',')
        return [t.strip() for t in tags if t]


class TagsInputWidget(TagsInputWidgetBase):
    class Media:
        css = {'all': ('lwt/css/jquery.tagsinput-revisited.css',)
               }
        js = ('lwt/js/_jquery.tagsinput-revisited.js',)


class AdminTagsInputWidget(
        widgets.FilteredSelectMultiple, TagsInputWidgetBase):
    # This class inherits FilteredSelectMultiple because the Django admin
    # handles the FilteredSelectMultiple differently from regular widgets

    @property
    def media(self):
        return forms.Media(js=self.Media.js, css=self.Media.css)

    class Media:
        css = getattr(settings, 'TAGS_INPUT_ADMIN_CSS', {'all': ('lwt/css/jquery.tagsinput-revisited.css',),})
        js = getattr(settings, 'TAGS_INPUT_ADMIN_JS', ('js/_jquery.tagsinput-revisited.js',))

