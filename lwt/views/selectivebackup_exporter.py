# django:
from django.core.serializers import serialize
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db import transaction
from django.db.models import Q, Value, Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.apps import apps
# second party
import os
import gzip
import io
import tempfile
# third party
# local
from lwt.models import *
from lwt.forms import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from lwt.views._nolang_redirect_decorator import *
from lwt.views._import_oldlwt import *
from lwt.views.termform import _create_curlybrace_sentence


''' backup the selective words (words checked in the term_list'''
def selectivebackup_exporter(request):
    checked_words = Words.objects.filter(owner=request.user, state=True).order_by('language').all()
    # we export also all the dependencies for a word. When importing, if duplicate,...
    #... they can be ignored
    words_with_dep = []
    for wo in checked_words:
        words_with_dep.append(wo.language)
        if wo.text:
            words_with_dep.append(wo.text)
        if wo.sentence:
            words_with_dep.append(wo.sentence)
        # When exporting, verify that all word has a customsentence (if not a sentence)
        if not wo.customsentence:
            wo.customsentence = _create_curlybrace_sentence(wo) 
            
        if wo.compoundword:
            words_with_dep.append(wo.compoundword)
        if wo.grouper_of_same_words:
            words_with_dep.append(wo.grouper_of_same_words)
        for wotag in wo.wordtags.all():
            words_with_dep.append(wotag)
        words_with_dep.append(wo)
    # ... and remove duplicates (since words can be linked to the same text, which has been added each time)
    words_with_dep = list(set(words_with_dep))
    # the Model to be imported must be in a specific order
    alphabet = {Languages: 0, Texts: 1, Sentences: 2, Grouper_of_same_words: 3, Wordtags: 4, Words: 5}
#     sort(['RL','HH','DA','AH'], 
#          key=lambda word: [alphabet.get(c, ord(c)) for c in word])
    words_with_dep.sort(key=lambda el: alphabet.get(type(el)) )
        
    fixture = serialize('yaml', words_with_dep, use_natural_foreign_keys=True, use_natural_primary_keys=True)

    now = timezone.now().strftime('%Y-%m-%d_%Hh%M') 
    filename = 'lingl_selectivebackup_{}.yaml.gz'.format(now)
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode='w') as f:
        f.write(fixture.encode())

    response = HttpResponse(out.getvalue(), content_type='application/gzip')
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response
