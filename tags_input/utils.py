from django.conf import settings
from django.db import models
from functools import partial as curry
#  curry function: it lets you take function with pre-defined arguments 
# and save it as a new function to use later only with needed arguments. 
# All this without running the function. 

from . import exceptions


def get_mappings():
    ''' Get all mappings from the settings To use the Django Tags Input module 
    the `TAGS_INPUT_SETTINGS` must be defined in Settings. 
    TAGS_INPUT_MAPPINGS = { 'lwt.Texttags':      {'field': 'txtagtext', 'create_missing': True},
                            'lwt.Wordtags':      {'field': 'wotagtext', 'create_missing': True},
                            'lwt.Texts':         {'field': 'txtitle'  , 'queryset'      : text_get_queryset},
                            'lwt.Words':         {'field': 'wotext'   , 'queryset'      : word_get_queryset},
                            '''
    return getattr(settings, 'TAGS_INPUT_MAPPINGS', {})


def get_mapping(model_or_queryset):
    ''' called by the Field at __init__():   utils.get_mapping(self.queryset)
    Get the mapping for a given model or queryset'''
    mappings = get_mappings()

    if isinstance(model_or_queryset, models.query.QuerySet):
        queryset = model_or_queryset
        model = model_or_queryset.model
    elif issubclass(model_or_queryset, models.Model):
        queryset = model_or_queryset.objects.all()
        model = model_or_queryset
    else:
        raise TypeError( 'Only `django.db.model.Model` and `django.db.query.QuerySet` objects are valid arguments')

    meta = model._meta
    mapping_key = meta.app_label + '.' + meta.object_name

    mapping = mappings.get(mapping_key)
    if mapping is not None:
        mapping = mapping.copy()
    else:
        raise exceptions.MappingUndefined('Unable to find mapping for %s' % mapping_key)

    # The callable allows for customizing the queryset on the fly
    queryset = mapping.get('queryset', queryset)
    if callable(queryset):
        queryset = queryset(mapping)

    mapping['app'] = meta.app_label
    mapping['model'] = meta.object_name
    mapping['queryset'] = queryset
    mapping.setdefault('separator', ' - ')

    if 'field' in mapping:
        mapping['fields'] = mapping['field'],
    elif 'fields' not in mapping:
        raise exceptions.ConfigurationError(
            'Every mapping should have a field or fields attribute. Mapping: '
            '%r' % mapping)
    mapping.setdefault('split_func', curry( mapping.get('split_func', split_func),
                                            mapping['fields'],
                                            mapping['separator'],))
    mapping.setdefault('join_func', curry( mapping.get('join_func', join_func),
                                            mapping['fields'],
                                            mapping['separator'],))
    mapping.setdefault('filter_func', curry( mapping.get('filter_func', filter_func),
                                            mapping['fields'],
                                            mapping['separator'],)) 
    return mapping.copy()

def filter_func(fields, separator, values):
    filters = {}
    if values:
        values = [v.split(separator, len(fields)) for v in values]
        items = zip(fields, zip(*values))
        for field, value in items:
            filters['%s__in' % field] = value 
    return filters

def join_func(fields, separator, values):
    return values['pk'], separator.join(values[field] for field in fields)

def split_func(fields, separator, value):
    return dict(zip(fields, value.split(separator, len(fields))))

