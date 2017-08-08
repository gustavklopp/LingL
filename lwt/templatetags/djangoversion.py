""" Creating a custom template which allows to display django version in the template """
from django import template
from django import get_version

register = template.Library()
@register.simple_tag
def version_django():
    return get_version()
   
