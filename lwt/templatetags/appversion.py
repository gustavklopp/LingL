""" Creating a custom template which allows to display the app version in the template """
from django import template

register = template.Library()
@register.simple_tag
def version_date():
    return "2021/04/22, 0.2.0"
   # return time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime('../.git')))
   
