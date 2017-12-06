from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from . import widgets
from . import utils


class TagsInputField(forms.ModelMultipleChoiceField):
    ''' create the field which can be create in any form:
    for ex.: texttags = fields.TagsInputField( Texttags.objects.all(),
                                    create_missing=True,
                                    required=False)'''
    widget = widgets.TagsInputWidget # a Widget is how the Field will be rendered in HTML
    default_error_messages = {
        'list': _('Enter a list of values.'),
        'invalid_choice': _('Select a valid choice. %s is not one of the available choices.'),
        'invalid_pk_value': _('"%s" is not a valid value for a primary key.')
    }

    def __init__(self, queryset, **kwargs):
        self.create_missing = kwargs.pop('create_missing', False)
        self.mapping = kwargs.pop('mapping', None)
        super(TagsInputField, self).__init__(queryset, **kwargs)
        self.widget.mapping = self.get_mapping() # calls the function below

    def get_mapping(self):
        if not self.mapping:
            self.mapping = mapping = utils.get_mapping(self.queryset)
            mapping['queryset'] = self.queryset
            mapping['create_missing'] = (self.create_missing or mapping.get('create_missing', False)) 
        return self.mapping

    def clean(self, value): # required function when creating custom: check if the data are valid
        mapping = self.get_mapping()
        fields = mapping['fields']
        filter_func = mapping['filter_func']
        join_func = mapping['join_func']
        split_func = mapping['split_func']

        values = dict( join_func(v)[::-1] for v in self.queryset.filter(**filter_func(value)).values('pk', *fields))
        values = dict((k.lower(), v) for k, v in values.items())
        missing = [v for v in value if v.lower() not in values]
        if missing:
            if mapping['create_missing']:
                for v in value:
                    if v in missing:
                        o = self.queryset.model(**split_func(v))
                        o.clean()
                        o.save()
                        values[v.lower()] = o.pk
            else:
                raise ValidationError( self.error_messages['invalid_choice'],
                                                            code='invalid_choice',
                                                            params={'value': ', '.join(missing)},) 
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

