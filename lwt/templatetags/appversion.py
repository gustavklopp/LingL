""" Creating a custom template which allows to display the app version in the template """
from django import template

register = template.Library()
@register.simple_tag
def version_date():
    return "2017/08/05, 0.1"
   # return time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime('../.git')))
   
