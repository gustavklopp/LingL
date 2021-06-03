from django.conf import settings
from django import forms
from django.template.loader import render_to_string
from django import urls
from django.contrib.admin import widgets

try:  # pragma: no cover
    from collections import OrderedDict
except ImportError:  # pragma: no cover
    from django.utils.datastructures import SortedDict as OrderedDict


class TagsInputWidgetBase(forms.SelectMultiple):

    def __init__(self, on_add_tag=None, on_remove_tag=None, on_change_tag=None,
                 *args, **kwargs):
        self.on_add_tag = on_add_tag
        self.on_remove_tag = on_remove_tag
        self.on_change_tag = on_change_tag
        forms.SelectMultiple.__init__(self, *args, **kwargs)

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        '''Compatibility function for the behavior changes in Django 1.11+'''
        attrs = dict(base_attrs or {}, **kwargs)
        if extra_attrs:  # pragma: no cover
            attrs.update(extra_attrs)
        return attrs

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        context = self.build_attrs(attrs, name=name)
        context['on_add_tag'] = self.on_add_tag
        context['on_remove_tag'] = self.on_remove_tag
        context['on_change_tag'] = self.on_change_tag

        context['STATIC_URL'] = settings.STATIC_URL
        context['mapping'] = self.mapping
        context['autocomplete_url'] = urls.reverse(
            'tags_input:autocomplete',
            kwargs=dict(
                app=self.mapping['app'],
                model=self.mapping['model'],
                fields='-'.join(self.mapping['fields']),
            ),
        )

        if value:
            fields = self.mapping['fields']
            join_func = self.mapping['join_func']

            ids = []
            for v in value:
                if isinstance(v, int):
                    ids.append(v)

            values_map = OrderedDict(map(
                join_func,
                self.mapping['queryset']
                .filter(pk__in=ids)
                .values('pk', *fields)
                .order_by('pk')
            ))

            values = []
            for v in value:
                if isinstance(v, int):
                    values.append(values_map[v])
                else:
                    values.append(v)

            context['values'] = ', '.join(values)

        return render_to_string('tags_input_widget.html', context)

    def value_from_datadict(self, data, files, name):
        tags = data.get(name, '').split(',')
        incomplete = data.get(name + '_incomplete', '')
        if incomplete != data.get(name + '_default'):
            tags += incomplete.split(',')
        return [t.strip() for t in tags if t]


class TagsInputWidget(TagsInputWidgetBase):

    class Media:

        css = {
            'all': (
                'jquery.tagsinput-revisited-2.0.min.css',
            ),
        }
        js = (
            'jquery.tagsinput-revisited-2.0.min.js',
        )
        enable_jquery = getattr(settings, 'TAGS_INPUT_INCLUDE_JQUERY', True)
        if enable_jquery:  # pragma: no cover
            css['all'] += 'jquery-ui-1.12.1.min.css',
            js = (
                'jquery-3.2.1.min.js',
                'jquery-ui-1.12.1.min.js',
            ) + js


class AdminTagsInputWidget(
        widgets.FilteredSelectMultiple, TagsInputWidgetBase):
    # This class inherits FilteredSelectMultiple because the Django admin
    # handles the FilteredSelectMultiple differently from regular widgets

    @property
    def media(self):
        return forms.Media(js=self.Media.js, css=self.Media.css)

    class Media:

        css = getattr(settings, 'TAGS_INPUT_ADMIN_CSS', {
            'all': (
                'jquery.tagsinput-revisited-2.0.min.css',
                'jquery-ui-1.12.1.min.css',
            ),
        })
        js = getattr(settings, 'TAGS_INPUT_ADMIN_JS', (
            'jquery-3.2.1.min.js',
            'jquery-ui-1.12.1.min.js',
            'jquery.tagsinput-revisited-2.0.min.js',
        ))

