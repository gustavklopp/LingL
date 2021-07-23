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

############ LINE_PROFILER ###############
# import line_profiler
# profile = line_profiler.LineProfiler()

def seltext_to_splittext(webpage, seltext, webpagesection, max_sentenceorder, iframe_html): 
    sentenceorder = max_sentenceorder +1
#     import pydevd; pydevd.settrace()
    seltext = html.unescape(seltext) # because it can have '&nbsp' inside.
    max_sentenceorder = splitText(webpage, seltext, webpagesection, sentenceorder)
    seltext_tag = '<span class="webpage_done" data-webpagesection="{}"></span>'.\
                    format(webpagesection)
    webpagesection += 1
    # and replace in the original iframe_html:
    iframe_html = re.sub(r'<span class="webpage_seltext">.*?</span>', seltext_tag, 
                        iframe_html, count=1) 
    return max_sentenceorder, iframe_html, webpagesection

''' display the webpage to be read'''
@login_required
@nolang_redirect
# @profile
def webpage_read(request, text_id=None):
    # User has selected text inside the webpage:
    if request.method == 'POST':
        iframe_html = request.POST['iframe_html'] # the entire HTML webpage is transmitted
        text_id = request.POST['text_id']
        webpage = Texts.objects.get(id=text_id)

        # In database, get what is the max webpagesection for this webpage if it exists:
        wos =  Words.objects.filter(text=webpage)
        max_webpagesection = wos.aggregate(Max('webpagesection'))['webpagesection__max'] if wos else -1
        # In database, get what is the max sentence Order for this webpage if it exists:
        sents =  Sentences.objects.filter(text=webpage)
        # we use the max_sentenceorder because each time the 'LingLibrify' is called, we need
        # to increase the index: 
        max_sentenceorder = sents.aggregate(Max('order'))['order__max'] if sents else -1

        webpagesection = max_webpagesection + 1
#         # BeautifulSoup version: Too slow!
#         soup = BeautifulSoup(iframe_html, 'lxml')
#         webpage_seltexts = soup.findAll('span', {'class':'webpage_seltext'})
#         for seltext_obj in webpage_seltexts:
#             sel_text = seltext_obj.text
#             sentenceorder = max_sentenceorder +1
#             max_sentenceorder = splitText(webpage, sel_text, webpagesection, sentenceorder)
#             seltext_obj.string = ''
#             seltext_obj['class'] = 'webpage_done'
#             seltext_obj['data-webpagesection'] = webpagesection # Next time this part won't be processed
#             webpagesection += 1
#         webpage.text = str(soup)
        # REGEX version:
        webpage_seltexts = re.findall(r'<span class="webpage_seltext">(.*?)</span>', iframe_html)

#         import multiprocessing as mp
#         from concurrent.futures import ProcessPoolExecutor 
#         from itertools import repeat
#         from ctypes import c_char_p
        
        # multiprocessing version:
#         with mp.Manager() as manager:
#             webpagesection = manager.Value(int, webpagesection)
#             max_sentenceorder = manager.Value(int, max_sentenceorder)
#             iframe_html = manager.Value(c_char_p, iframe_html)
#             zipped_args = zip( repeat(webpage),
#                             webpage_seltexts,
#                            repeat(webpagesection),
#                            repeat(max_sentenceorder),
#                            repeat(iframe_html)
#                            )
#             with manager.Pool() as pool:
             # standard manager.Pool is NOT ALLOWED: 'Daemonic processes are not allowed to have children'
#             with ProcessPoolExecutor() as pool: # NOT WORKING... when calling splittext, the process seems to stop
#                 pool.map(mp_seltext_to_splittext, *zip(*zipped_args))

#             webpage.text = iframe_html.value

        # non-multiprocessing version:
        for seltext in webpage_seltexts:
            max_sentenceorder, iframe_html, webpagesection = seltext_to_splittext(webpage, seltext, webpagesection, max_sentenceorder, iframe_html)
        webpage.text = iframe_html

        webpage.save()

        #update the cookie for the database_size
        set_word_database_size(request)

    # Display the already processed text (which is stored in text.text in fact)
    elif request.method == 'GET':
        webpage = Texts.objects.get(id=text_id)

    webpage_html = webpage.text
    url = webpage.title
    bottomleft = escape(webpage_html)
        
    previoustext, nexttext, todo_wordcount, todo_wordcount_pc, texttotalword,\
    word_inthistext, statuses, wordtags, texttags = _textANDwebpage_common(request, webpage, text_id)

#     # OUTPUT THE LINE_PROFILER
#     with open('output.txt', 'w') as stream:
#         profile.print_stats(stream=stream)
    
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
