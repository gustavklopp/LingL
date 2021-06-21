# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db.models import Q, Value, Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.serializers import serialize
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import ugettext as _
# second party

# third party)
# local
from lwt.models import *
from lwt.forms import ProfileForm

# helper functions:
from lwt.views._utilities_views import get_word_database_size, get_appversion




@login_required
def profile(request):
    # display the profile's information
    if request.method == 'GET':
        user = MyUser.objects.get(id=request.GET['id'])
        if user != request.user: # only the user can see his own profile
            return redirect(reverse('homepage'))

        f = ProfileForm(instance = user) 

        # get the current database size:
        database_size = get_word_database_size(request)
        # get the appversion:
        appversion = get_appversion(request)

        return render(request, 'lwt/profile.html', {'form': f, 'database_size':database_size, 'appversion':appversion })
    
    # processing the form
    elif request.method == 'POST':
        user = MyUser.objects.get(id=request.GET['id'])
        f = ProfileForm(request.POST, instance=user) 
        if f.is_valid():
            f.save(commit=True)

            # the user languages needs the correct dict URIs with the User's origin lang:
            for lang in Languages.objects.filter(owner=request.user):
                lang = substitute_in_dictURI(request.user, lang, called_by_Obj=True)
                # and put it in dict1uri and dict2uri also
                dicturi = lang.dicturi.split(',')
                lang.dict1uri = dicturi[0].strip()
                lang.dict2uri = dicturi[1].strip()
                lang.save()

            messages.add_message(request, messages.SUCCESS, _('Profile successfully edited'))
            return redirect(reverse('homepage'))
        else:
            f = ProfileForm(instance = user) 
            # get the current database size:
            database_size = get_word_database_size(request)
            # get the appversion:
            appversion = get_appversion(request)

            messages.add_message(request, messages.ERROR, _('Please correct this'))
            return render(request, 'lwt/profile.html', {'form': f, 'database_size':database_size, 'appversion':appversion })


