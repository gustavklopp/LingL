from django import forms

from . import widgets


class SplitJSONField(forms.Field):
    ''' create the field which can be create in any form:'''

    widget = widgets.SplitJSONWidget # a Widget is how the Field will be rendered in HTML

    def clean(self, value): # required function when creating custom: check if the data are valid
        return value