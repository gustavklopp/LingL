# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db import transaction
from django.db.models import Q
from django.templatetags.i18n import language
from django.http.response import JsonResponse
from django.http import JsonResponse, HttpResponse #used for ajax
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils.translation import ngettext 
from django.templatetags.static import static # to use the 'static' tag as in the templates
from django.db.models import Max
from django.template import Template, Context 
# second party:
import json
import datetime
import re
import platform
# third party
from urllib.request import Request, urlopen # use to scrap the dictionary
from urllib.parse import urljoin, urlparse
import html # use to scrap the dictionary
from bs4 import BeautifulSoup #use to scrap
# local
from lwt.models import *
# helper functions:
from lwt.views._nolang_redirect_decorator import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from lwt.views.text_read import _textANDwebpage_common
from lwt.constants import STATUS_CHOICES

''' display the webpage to be read'''
@login_required
@nolang_redirect
def webpage_read(request, text_id=None):
    # User has selected text inside the webpage:
    if request.method == 'POST':
        iframe_html = request.POST['iframe_html']
        text_id = request.POST['text_id']
        webpage = Texts.objects.get(id=text_id)

        # get what is the max webpagesection for this webpage if it exists:
        wos =  Words.objects.filter(text=webpage)
        max_webpagesection = wos.aggregate(Max('webpagesection'))['webpagesection__max'] if wos else -1
        # get what is the max sentence Order for this webpage if it exists:
        sents =  Sentences.objects.filter(text=webpage)
        max_sentenceorder = sents.aggregate(Max('order'))['order__max'] if sents else -1

        soup = BeautifulSoup(iframe_html, 'html.parser')
        webpage_seltexts = soup.findAll('span', {'class':'webpage_seltext'})
        webpagesection = max_webpagesection + 1
        for seltext_obj in webpage_seltexts:
            sel_text = seltext_obj.text
            sentenceorder = max_sentenceorder +1
            max_sentenceorder = splitText(webpage, sel_text, webpagesection, sentenceorder)
            seltext_obj.string = ''
            seltext_obj['class'] = 'webpage_done'
            seltext_obj['data-webpagesection'] = webpagesection # Next time this part won't be processed
            webpagesection += 1
        webpage.text = str(soup)
        webpage.save()

        #update the cookie for the database_size
        set_word_database_size(request)

    # Display the already processed text (which is stored in text.text in fact)
    elif request.method == 'GET':
        webpage = Texts.objects.get(id=text_id)

    html = webpage.text
    url = webpage.title
    bottomleft = escape(html)
        
    previoustext, nexttext, todo_wordcount, todo_wordcount_pc, texttotalword,\
    word_inthistext, statuses, wordtags, texttags = _textANDwebpage_common(request, webpage, text_id)

    return render(request, 'lwt/webpage_read.html', { 
                'text':webpage,
                'previoustext':previoustext,'nexttext':nexttext,
                'todo_wordcount': todo_wordcount, 'todo_wordcount_pc':todo_wordcount_pc,
                                                'texttotalword':texttotalword,
                # inside thetext div:
                'word_inthistext':word_inthistext,
                # for tooltip
                'statuses':statuses,'wordtags':wordtags,'texttags':texttags,
                # specific webpage:
                'bottomleft':bottomleft, 'url':url, 'text_type': 'webpage'
        })
