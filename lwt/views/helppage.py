# -*- coding: utf-8 -*-
# django:
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
 
    return render(request, 'lwt/helppage.html',{'database_size':database_size})
