from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import widgets
from . import utils


class TagsInputField(forms.ModelMultipleChoiceField):
    widget = widgets.TagsInputWidget
    default_error_messages = {
        'list': _('Enter a list of values.'),
        'invalid_choice': _('!!!Select a valid choice. %s is not one of the'
                            ' available choices.'),
        'invalid_pk_value': _('"%s" is not a valid value for a primary key.')
    }

    def __init__(self, queryset, **kwargs):
        self.create_missing = kwargs.pop('create_missing', False)
        self.mapping = kwargs.pop('mapping', None)
        super(TagsInputField, self).__init__(queryset, **kwargs)
        self.widget.mapping = self.get_mapping(owner=None)

    def get_mapping(self, owner):
        if not self.mapping:
            # utils.get_mapping get the value of 'TAGS_INPUT_MAPPINGS' in settings.py
            self.mapping = mapping = utils.get_mapping(self.queryset, owner)
            mapping['queryset'] = self.queryset
            mapping['create_missing'] = ( self.create_missing or mapping.get('create_missing', False))

        return self.mapping

    def clean(self, value): #validation (when calling: f.is_valid() )
        mapping = self.get_mapping(self.owner)
#         mapping = {'field': 'txtagtext', 
#              'create_missing': False, 
#              'app': 'lwt', 'model': 'Texttags', 
#              'queryset': <QuerySet []>, 
#              'separator': ' - ', 
#              'fields': ('txtagtext',), 
#              'split_func': functools.partial(<function split_func at 0x7fdae865cdc0>, ('txtagtext',), 
#                         ' - '), 
#              'join_func': functools.partial(<function join_func at 0x7fdae865cd30>, ('txtagtext',), 
#                      ' - '), 
#              'filter_func': functools.partial(<function filter_func at 0x7fdae865cca0>, ('txtagtext',),
#                     ' - ')
#         }
        fields = mapping['fields'] #  ('txtagtext',) 
        filter_func = mapping['filter_func'] #  functools.partial(<function filter_func at 0x7fdae865cca0>, ('txtagtext',)                     ' - ')
        join_func = mapping['join_func']
        split_func = mapping['split_func']

        # Retrieve all the tags in the database:
        # it creates a dict: {'4': <mytag>, '7':<myothertag>...} with the '4', '7' is the pk
        values = dict(
            join_func(v)[::-1] for v in self.queryset
            .filter(**filter_func(value))
            .filter(owner=self.owner)
            .values('pk', *fields)
        ) # = {}
        values = dict((k.lower(), v) for k, v in values.items()) # lowercase all keys
        # create the tag which are not found
        missing = [v for v in value if v.lower() not in values]
        if missing:
            if mapping['create_missing']:
                for v in value: # value = ['mytagtext','myothertagtext',...]
                    if v in missing:
                        args = split_func(v)
                        args['owner_id'] = self.owner.id
                        o = self.queryset.model(**args)
                        o.clean()
                        o.save()
                        values[v.lower()] = o.pk
            else:
                pass
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': ', '.join(missing)},
                )

        ids = []
        for v in value:
            ids.append(values[v.lower()])

        return forms.ModelMultipleChoiceField.clean(self, ids)


class AdminTagsInputField(TagsInputField):
    widget = widgets.AdminTagsInputWidget

    def __init__(self, queryset, verbose_name=None, *args, **kwargs):
        TagsInputField.__init__(self, queryset, *args, **kwargs)

        if verbose_name:  # pragma: no branch
            self.label = verbose_name

