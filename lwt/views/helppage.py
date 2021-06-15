# -*- coding: utf-8 -*-
# django:
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# third party
import platform
# helper functions:
from lwt.views._nolang_redirect_decorator import *
from lwt.views._utilities_views import get_word_database_size

''' display the keyboard shortcuts
    TODO maybe add possibility to customize the shortcuts???
'''
@login_required
@nolang_redirect
def helppage(request):
    # get the current database size:
    database_size = get_word_database_size(request)

    # detect if mac or else
    system = platform.system().lower()
    if system == 'windows' or system == 'linux': 
        is_Mac = False
    else:
        is_Mac = True

    return render(request, 'lwt/helppage.html',{'is_Mac':is_Mac, 'database_size':database_size})
