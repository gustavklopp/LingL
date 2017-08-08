# django:
from django.shortcuts import render
from django.template import context
from django.template.loader import get_template
from django.db.models import F, Value, Count
# third party
# local
from lwt.models import Settings
from lwt.models import Languages
from lwt.models import Texts
from lwt.models import Archivedtexts
from lwt.models import Words
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language

# Home Page
def homepage(request):
#     # get the last opened file and last used language in Settings: Return a None variable if they do not exist
#     # Don't forget to cast to int the ID fetched from the Settings table!
#     try:
#         currentlang_id = int(Settings.objects.values_list('stvalue',flat=True).get(stkey='currentlanguage'))
#         currentlang_name = Languages.objects.values_list('lgname',flat=True).get(lgid=currentlang_id)
#     except ObjectDoesNotExist:
#         currentlang_name = None
    # the same, with cookie:
    currentlang_name = request.session.get('currentlang_name', None)
         
    try:
        currenttext_id = int(Settings.objects.values_list('stvalue',flat=True).get(stkey='currenttext'))
        currenttext = Texts.objects.get(txid=currenttext_id)
    except ObjectDoesNotExist:
        currenttext = None
         
    # get the list of languages to display them in the drop-down menu:
    language_selectoption = Languages.objects.values('lgname','lgid').order_by('lgname')
    
    return render(request, 'lwt/homepage.html', {'currentlang_name':currentlang_name,
                                                'currenttext':currenttext,
                                                'language_selectoption':language_selectoption})

# all of the Texts list in the selected langugage
def text_list(request):
    return render (request, 'lwt/text_list.html')

# text read
def text_detail(request,message_key,message_val):
    """
      ... markaction=[opcode] ... do actions on marked texts
      ... del=[textid] ... do delete
      ... arch=[textid] ... do archive
      ... op=Check ... do check
      ... op=Save ... do insert new 
      ... op=Change ... do update
      ... op=Save+and+Open ... do insert new and open 
      ... op=Change+and+Open ... do update and open
      ... new=1 ... display new text screen 
      ... chg=[textid] ... display edit screen 
      ... filterlang=[langid] ... language filter 
      ... sort=[sortcode] ... sort 
      ... page=[pageno] ... page  
      ... query=[titlefilter] ... title filter
      """ 
    # get the current language 
    currentlang_name = request.session.get('currentlang_name')
    # get the list of languages to display them in the drop-down menu:
    language_selectoption = Languages.objects.values('lgname','lgid').order_by('lgname')
        
    # a new text is created:
    if message_key == 'new':
        
    return render(request, 'lwt/text_detail.html', {'currentlang_name':currentlang_name,
                                                    'language_selectoption':language_selectoption,
                                                    })

# test the text
def text_test(request):
    return render(request, 'lwt/text_test.html')

# print the text
def text_print(request):
    return render(request, 'lwt/text_print.html')

# print improved annoted text: No IDEA WHAT IT IS...
def text_improved_print(request):
    return render(request, 'lwt/text_improved_print.html')

# archived texts list
def archivedtext_list(request): 
    return render(request, 'lwt/archivedtest_list.html')

# archived texts list
def archivedtext_detail(request): 
    return render(request, 'lwt/archivedtest_detail.html')

# text tags list
def texttag_list(request):
    return render(request, 'lwt/texttag_list.html')

# languages list
def language_list(request, message_key=None, message_val=None):

    if request.method == 'POST':
        message_key = request.POST.get('message_key')
        message_val = request.POST.get('message_val')
        lgname = request.POST.get('lgname')
        lgdict1uri = request.POST.get('lgdict1uri')
        lgdict2uri = request.POST.get('lgdict2uri')
        lggoogletranslateuri = request.POST.get('lggoogletranslateuri')
        lgexporttemplate = request.POST.get('lgexporttemplate')
        lgtextsize = request.POST.get('lgtextsize')
        lgcharactersubstitutions = request.POST.get('lgcharactersubstitutions')
        lgregexpsplitsentences = request.POST.get('lgregexpsplitsentences')
        lgexceptionssplitsentences = request.POST.get('lgexceptionssplitsentences')
        lgregexpwordcharacters = request.POST.get('lgregexpwordcharacters')
        lgremovespaces = request.POST.get('lgremovespaces')
        lgspliteachchar = request.POST.get('lgspliteachchar')
        lgrighttoleft = request.POST.get('lgrighttoleft')
        # new language:
        if message_key == 'new':
            lang = Languages(
                lgname=lgname,lgdict1uri=lgdict1uri,lgdict2uri=lgdict2uri,lggoogletranslateuri=lggoogletranslateuri,
                lgexporttemplate=lgexporttemplate,lgtextsize=lgtextsize,lgcharactersubstitutions=lgcharactersubstitutions,
                lgregexpsplitsentences=lgregexpsplitsentences,lgexceptionssplitsentences=lgexceptionssplitsentences,
                lgregexpwordcharacters=lgregexpwordcharacters,lgremovespaces=lgremovespaces,lgspliteachchar=lgspliteachchar,
                lgrighttoleft=lgrighttoleft)
            lang.save()

            # set this new language as automatically the current language. Create the stkey/stvalue if it doesn't exist
            try:
                Settings.objects.update(stkey='currentlang_id',stvalue=lang.lgid).save()
            except: # if in the settings, current language has never been created
                Settings(stkey='currentlang_id',stvalue=lang.lgid).save()
            # and change the cookie:
            request.session['currentlang_name'] = lang.lgname
            request.session['currentlang_id'] = lang.lgid

        # editing an existing language:
        if message_key == 'edit':
            lang = Languages.objects.filter(lgid=message_val).update(
                lgname=lgname,lgdict1uri=lgdict1uri,lgdict2uri=lgdict2uri,lggoogletranslateuri=lggoogletranslateuri,
                lgexporttemplate=lgexporttemplate,lgtextsize=lgtextsize,lgcharactersubstitutions=lgcharactersubstitutions,
                lgregexpsplitsentences=lgregexpsplitsentences,lgexceptionssplitsentences=lgexceptionssplitsentences,
                lgregexpwordcharacters=lgregexpwordcharacters,lgremovespaces=lgremovespaces,lgspliteachchar=lgspliteachchar,
                lgrighttoleft=lgrighttoleft)

    # make the language currentlanguage. For example with the icon in Language_list
    if message_key == 'setcurrent': 
        Settings.objects.update(stkey='currentlanguage',stvalue=message_val)
        # and edit cookies:
        request.session['currentlang_id'] = message_val
        request.session['currentlang_name'] = Languages.objects.values_list('lgname',flat=True).get(lgid=message_val)
        
    #TODO:
    if message_key == 'refresh':
        pass
    
    if message_key == 'delete':
        pass

    all_languages = Languages.objects.all().order_by('lgname')

    # currentlang_id variable set to None if the Languages table is empty:
#     try: 
#         currentlang_id = int(Settings.objects.values_list('stvalue',flat=True).get(stkey='currentlanguage'))
#     except ObjectDoesNotExist:
#         currentlang_id = None
    # the same with cookie:
    currentlang_id = request.session.get('currentlang_id', None)

    # append also the number of texts/words/archived text, for each language
    Texts.objects.annotate(textcount=Value(Texts.objects.count(),output_field=IntegerField()))
    Archivedtexts.objects.annotate(archtextcount=Value(Archivedtexts.objects.count(),output_field=IntegerField()))
    Words.objects.annotate(termcount=Value(Words.objects.count(),output_field=IntegerField()))

    return render(request, 'lwt/language_list.html',{'all_languages':all_languages,
                                                     'currentlang_id':currentlang_id})

# languages detail: edit/create a language
def language_detail(request, message_key=None, message_val=None):
    # GET method to see what the user wants to do on this page:
    message = {'key':message_key,'val':message_val}
    # a new language is requested:
    if message_key == 'new':
        lang = None
    if message_key == 'edit':
        lang = Languages.objects.get(lgid=message_val)
    # get all the languages (used for javascript script to check no doublon)
    all_languages = Languages.objects.all()
    return render(request, 'lwt/language_detail.html', {'all_languages':all_languages,
                                                        'lang':lang})

# terms list
def term_list(request):
    return render(request, 'lwt/term_list.html')

# term detail:
def term_detail(request):
    return render(request, 'lwt/term_detail.html')

# term tag list
def termtag_list(request):
    return render(request, 'lwt/termtag_list.html')

# statistics
def statistics(request):
    return render(request, 'lwt/statistics.html')

# Check text
def textcheck(request):
    return render(request, 'lwt/textcheck.html')

# Long text import
def longtextimport(request):
    return render(request, 'lwt/longtextimport.html')

# Term import
def termimport(request):
    return render(request, 'lwt/termimport.html')

# Backup/restore
def backuprestore(request):
    return render(request, 'lwt/backuprestore.html')

# settings
def settings(request):
    return render(request, 'lwt/settings.html')

# help
def help(request):
    return render(request, 'lwt/help.html')

# installing a demo version of the database
def install_demo(request):
    return render(request, 'lwt/install_demo.html')

# Test whether the terms are known
def do_test(request):
    return render(request, 'lwt/do_test.html')