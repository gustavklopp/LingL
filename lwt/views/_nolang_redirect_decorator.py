from django.http import HttpResponseRedirect
from django.urls import reverse
# helper functions:
from lwt.views._setting_cookie_db import *


def nolang_redirect(func):
    ''' redirect to homepage (where the user can then defined his first language, if the 
    language has not been set, i.e no cookie for currentlang '''
    def wrap(request, *args, **kwargs):
        stvar = getter_settings_cookie_else_db('currentlang_id', request)
        if stvar == '':
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return func(request, *args, **kwargs)
    return wrap