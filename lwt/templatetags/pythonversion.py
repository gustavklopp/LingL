""" Creating a custom template which allows to display python version in the template """
from django import template
from platform import python_version

register = template.Library()
@register.simple_tag
def version_python():
    return python_version()