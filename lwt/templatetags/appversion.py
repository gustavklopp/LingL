""" Creating a custom template which allows to display the app version in the template """
from django import template

register = template.Library()
@register.simple_tag
def version_date():
    with open('appversion.txt', encoding="utf8", 'r') as appversion_f:
        appversion = appversion_f.read()
        return appversion
        # return time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime('../.git')))
   
