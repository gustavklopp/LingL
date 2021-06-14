# django:
from django.core.serializers import serialize
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db import transaction
from django.db.models import Q, Value, Count
from django.db.models.functions import Lower 
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

''' because the \t character in the database is recovered as a '\\t' '''
def _unescape_special_char(text):
    return text.replace('\\t', '\t')

''' download the txt file with anki formated words'''
def export2anki_exporter(request):
    anki_words = Words.objects.filter(owner=request.user, state=True).order_by('language').all()
    language = anki_words.first().language
    anki = ''
    for wo in anki_words.prefetch_related('wordtags'): # 'prefetch_related': because it's a m2m relationshi:
        if wo.language != language: # each languge can have its own template
            language = wo.language
        exporttemplate = language.exporttemplate
        exporttemplate = _unescape_special_char(exporttemplate)
        exporttemplate = exporttemplate.replace('$status', str(wo.status))
        exporttemplate = exporttemplate.replace('$language', wo.language.name)
        exporttemplate = exporttemplate.replace('$text', wo.text.title)
        if wo.sentence:
            exporttemplate = exporttemplate.replace('$sentence', wo.sentence.sentencetext)
        else:
            exporttemplate = exporttemplate.replace('$sentence', '')
        if wo.wordtext:
            exporttemplate = exporttemplate.replace('$word', wo.wordtext)
        else:
            exporttemplate = exporttemplate.replace('$word', '')
        if wo.translation and wo.translation != 'NULL': # NULL because of the importer from old lwt
            exporttemplate = exporttemplate.replace('$translation', wo.translation)
        else:
            exporttemplate = exporttemplate.replace('$translation', '')
        if wo.romanization and wo.romanization != 'NULL': # NULL because of the importer from old lwt
            exporttemplate = exporttemplate.replace('$romanization', wo.romanization)
        else:
            exporttemplate = exporttemplate.replace('$romanization', '')
        if wo.customsentence and wo.customsentence != 'NULL':
            exporttemplate = exporttemplate.replace('$customsentence', wo.customsentence)
        else:
            exporttemplate = exporttemplate.replace('$customsentence', '')
        wordtags = [' '+wt.wotagtext for wt in wo.wordtags.all()]
        exporttemplate = exporttemplate.replace('$tags', ','.join(wordtags))
        if wo.compoundword:
            compoundword = [' '+cw.wordtext for cw in wo.compoundword.compoundwordhavingthiswordinside.all()]
            exporttemplate = exporttemplate.replace('$compoundword', ','.join(compoundword))
        else:
            exporttemplate = exporttemplate.replace('$compoundword', '')
        similarword = [' '+sm.wordtext for sm in wo.grouper_of_same_words.grouper_of_same_words_for_this_word.all()]
        exporttemplate = exporttemplate.replace('$similarword', ','.join(similarword))
        if wo.extra_field:
            extra_field_kv = ''
            extra_field_list = json.loads(wo.extra_field)
            for idx, extra in enumerate(extra_field_list):
                if idx != 0:
                    extra_field_kv += '\n'
                k = list(extra.keys())[0]
                v = list(extra.values())[0]
                r += k + ': ' + v
            exporttemplate = exporttemplate.replace('$extra_field', extra_field_kv)
        else:
            exporttemplate = exporttemplate.replace('$extra_field', '')
        anki += exporttemplate + '\n'
        
    response = HttpResponse(anki, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={}'.format('lingl_words_for_anki.txt')
    return response
