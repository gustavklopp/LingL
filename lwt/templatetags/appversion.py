""" Creating a custom template which allows to display the app version in the template """
import os
from django.conf import settings
from django import template

register = template.Library()
@register.simple_tag
def version_date():
    appversiontxt_path = os.path.join(settings.BASE_DIR, 'lwt', 'appversion.txt')
    with open(appversiontxt_path, 'r', encoding="utf8") as appversion_f:
        appversion = appversion_f.read()
        return appversion
        # return time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime('../.git')))
   
