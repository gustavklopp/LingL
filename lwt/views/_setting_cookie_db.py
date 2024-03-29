# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db.models import Q, Value, Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language
from  django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # used for pagination (on text_list for ex.)
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
# third party
# local

""" Helper functions. """


def setter_settings_cookie_and_db(stkey, stvalue, request, owner=None):
    """ set the setting value set by user in key in Cookie and also set it in Settings database """
    from lwt.models import Settings_currentlang_id, Settings_currentlang_name, Languages

    if owner == None: # if it's not defined elsewhere (for example when restoring database
        owner = request.user
    model_name = 'Settings_'+str(stkey)

    # special case when setting of curent lang: (we need to update ´id´ and ´name´
    if model_name == 'Settings_setcurrentlang':
        # and put currentlang_name too:
        if int(stvalue) == -1: # code for: No languages to filter on
            currentlang_name = -1
        else:
            currentlang_name = Languages.objects.filter(owner=owner).values_list('name',flat=True).get(id=stvalue)
        # put in Settings table
        Settings_currentlang_id.objects.filter(owner=owner).\
                            update_or_create(defaults={'stvalue':stvalue, 'owner':owner})
        Settings_currentlang_name.objects.filter(owner=owner).\
                            update_or_create(defaults={'stvalue':currentlang_name, 'owner':owner})
        # and edit cookies:
        request.session['currentlang_name'] = currentlang_name
        request.session['currentlang_id'] = stvalue

    else:
        currentset = apps.get_model('lwt', model_name)
        # put in Settings table
        currentset.objects.filter(owner=owner).\
                                            update_or_create(defaults={'stvalue':stvalue, 'owner':owner})
        # and edit cookies:
        request.session[str(stkey)] = stvalue

        
""" set the setting value set by user in key in Cookie only """
def setter_settings_cookie(stkey, stvalue,request):
    request.session[stkey] = stvalue

''' same as func above setter_settings_cookie but which set also in database
    in fact, it´s used only for currentlanguage_name and currentlanguage_id'''
# def setter_settings_db_and_cookie(stkey, stvalue, request, owner=None):
#     if owner == None: # if it's not defined elsewhere (for example when restoring database
#         owner = request.user
#     model_name = 'Settings_'+str(stkey)
#     currentset = apps.get_model('lwt', model_name)
#     # put in Settings table
#     currentset.objects.filter(owner=owner, stvalue=stvalue).\
#                                         update_or_create(defaults={'stvalue':stvalue, 'owner':owner})
#     # and set in cookie
#     request.session[stkey] = stvalue

def getter_settings_cookie(stkey, request):
    """ get the setting value set by user in key in Cookie if it was set"""
    if stkey in request.session.keys(): # it's in a Cookie?
        stvar = request.session.get(stkey)
    else:
        stvar = None # no cookie set
    # Converter to int if it's possible:
    if stvar and isinstance(stvar, str): # stvar is not "" or None and is a string
        if stvar.isdigit(): # then, check if it can be convert to digit 
                stvar = int(stvar)
    return stvar

''' same as func above getter_settings_cookie but which search in database
    in fact, it´s used only for currentlanguage_name and currentlanguage_id'''
def getter_settings_cookie_else_db(stkey,request):
    if stkey in request.session.keys(): # it's in a Cookie?
        stvar = request.session.get(stkey)
    else: # no cookie set for this key. Check in the database
        model_name = 'Settings_'+str(stkey)
        currentset = apps.get_model('lwt', model_name)
        try:
            stvar = currentset.objects.filter(owner=request.user).get().stvalue # the User has already set a value:
        except ObjectDoesNotExist: # else get the default 
            stvar = currentset._meta.get_field('stdft').get_default() 
    # Converter to int if it's possible:
    if stvar and isinstance(stvar,str): # stvar is not "" or None and is a string
        if stvar.isdigit(): # then, check if it can be convert to digit 
                stvar = int(stvar)
    return stvar

def getter_session_else_cookie(request,reqkey,sesskey,default='',isnum=True):
    """ get the setting value set by user in key in GET/POST method, else in Cookie 
    if it was set, else default """
    if reqkey in request.GET or reqkey in request.POST:
        # the GET/POST var has been set:
        reqdata = request.GET[reqkey] if reqkey in request.GET else request.POST[reqkey]
        request.session[sesskey] = reqdata #  put the result into COOKIE
        result = reqdata # and return also the result
    elif sesskey in request.session:
        result = request.session[sesskey]	
    else: 
        result = default
    result = int(result) if isnum else result
    return result

def getter_settings_db(request, stkey):
    """ get the setting value set by user, or else the default, in Settings database """
    model_name = 'Settings_' + stkey
    currentset = apps.get_model('lwt', model_name)

    try: # the User has already set a value:
        stvar = currentset.objects.filter(owner=request.user).get().stvalue
    except ObjectDoesNotExist: # else get the default 
        stvar = currentset._meta.get_field('stdft').get_default() 
    # Converter to int if it's possible:
    if stvar and isinstance(stvar,str): # stvar is not "" or None and is a string
        if stvar.isdigit(): # then, check if it can be convert to digit 
                stvar = int(stvar)
    return stvar