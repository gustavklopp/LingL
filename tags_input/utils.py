import functools

from django.conf import settings
from django.db import models

from . import exceptions



def get_mapping(model_or_queryset, owner):
    '''Get the mapping for a given model or queryset'''
    mappings = getattr(settings, 'TAGS_INPUT_MAPPINGS', {})  # get the mappings in settings.py

    if isinstance(model_or_queryset, models.query.QuerySet):
        queryset = model_or_queryset
        model = model_or_queryset.model
    elif issubclass(model_or_queryset, models.Model):
        queryset = model_or_queryset.objects.filter(owner=owner)
        model = model_or_queryset
    else:
        raise TypeError(
            'Only `django.db.model.Model` and `django.db.query.QuerySet` '
            'objects are valid arguments')

    meta = model._meta
    mapping_key = meta.app_label + '.' + meta.object_name

    mapping = mappings.get(mapping_key)
    if mapping is not None:
        mapping = mapping.copy()
    else:
        raise exceptions.MappingUndefined('Unable to find mapping '
                                          'for %s' % mapping_key)

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

#     NB About 'functools.partial': it allows to create a 'partial' function where arguments are missing:
#     def multiply(x,y):
#             return x * y
#     # create a new function that multiplies by 2
#     dbl = partial(multiply,2)
#     print(dbl(4)) # ==> 8
    
    mapping.setdefault('split_func', functools.partial( mapping.get('split_func', split_func),
                                                        mapping['fields'],
                                                        mapping['separator'],
                                                    ))
    mapping.setdefault('join_func', functools.partial( mapping.get('join_func', join_func),
                                                        mapping['fields'],
                                                        mapping['separator'],
                                                    ))
    mapping.setdefault('filter_func', functools.partial( mapping.get('filter_func', filter_func),
                                                        mapping['fields'],
                                                        mapping['separator'],
                                                    ))

    return mapping.copy()

''' it convert for ex.:
    print(filter_func( ('pk','owner'), '-', ('1-3','8-1'))) !!!pk and owner should have the same length
    ==> {'owner__in': ('3', '1'), 'pk__in': ('1', '8')} '''
def filter_func(fields, separator, values):
    filters = {}
    if values:
        values = [v.split(separator, len(fields)) for v in values]
        items = zip(fields, zip(*values))
        for field, value in items:
            filters['%s__in' % field] = value

    return filters


''' it convert for ex.:
    join_func(('txtagtext','pk'), '-', {'txtagtext':'my tag title','pk':'1'})
    ==> ('1', 'my tag title-1') '''
def join_func(fields, separator, values):
    return values['pk'], separator.join(values[field] for field in fields)

''' it converts for example:
    split_func( ('txtagtext','owner_id'), '-', 'my tag title-3') )
    ==> {'txtagtext':'my tag title', 'owner_id':'3'} '''
def split_func(fields, separator, value):
    return dict(zip(fields, value.split(separator, len(fields))))

