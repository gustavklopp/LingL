# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.db.models import Q, Value, Count
from django.db.models.functions import Lower 
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import CharField,IntegerField
from django.templatetags.i18n import language
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # used for pagination (on text_list for ex.)
from django.urls import reverse
from django.utils.translation import ugettext as _, ungettext as s_
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static # to use the 'static' tag as in the templates
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
# second party
from datetime import timedelta
# third party
# local
from lwt.models import *
from lwt.forms import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from lwt.views._nolang_redirect_decorator import *
from lwt.views._utilities_views import get_word_database_size

''''the checkboxes to filter the terms '''
def textlist_filter(request):
    limit = -1

    if 'limit' in request.POST.keys(): # number of rows to display per page
        limit = request.POST['limit']
        limit = int(limit)
    all_texts = Texts.objects.filter(owner=request.user).all()
    # then apply the filtering (it sets also the cookie). Func list_filtering is in lwt/views/_utilities_views.py
    all_texts = list_filtering(all_texts, request) 
    total = all_texts.count()
    all_texts = all_texts[:limit]
    all_texts = serialize_bootstraptable(all_texts,total)
    return JsonResponse(all_texts, safe=False)

''' called by ajax (built-in function) inside bootstrap-table #text_table to fill the table'''
def load_texttable(request):
    order, sort, sort_modif, offset, offset_modif, limit, limit_modif, all_texts = requesting_get_by_table(request, Texts)

    if 'search' in request.GET.keys():
        search = request.GET['search']
        if search != '': # when deleting the previous search, ajax will send the search word ''. consider it like No filter
            all_texts = all_texts.filter(title=search)
    # then apply the filtering (it sets also the cookie). Func list_filtering is in lwt/views/_utilities_views.py
    all_texts = list_filtering(all_texts, request) 
    
    total = all_texts.count() 
    
    all_texts_filtered = all_texts[offset_modif:offset_modif + limit_modif]
    data = []

#     def linked(word):
#         ''' create a link inside the bootstrap table: clicking on the word jump to the right place '''
#         st = '<a href="#" onclick="jumpToRow('
#         # calculate at which page and row is this word:
#         filter_kw = {'{}__lt'.format(sort) : getattr(word, sort)}
#         row_id = all_texts.filter(**filter_kw).count() # used to get the row in the table
#         row_per_page = limit_modif
#         page_id = row_id // row_per_page +1
#         row_id_inthepage = row_id - row_per_page*(page_id -1)
#          
#         st += str(page_id)+','+str(row_id_inthepage)+');">'
#         en = '</a>'
#         return st + word.wordtext + en

    # then zip it to the all_texts to loop inside it in the template
    for t in all_texts_filtered.prefetch_related('texttags'): # 'prefetch_related': because it's a m2m relationship
        t_dict = {}
        t_dict['id'] = t.id
        ##############################
        t_dict['read'] = '<a href="'+ reverse('text_read',args=[t.id]) + '"><img src="' + \
            static('lwt/img/icn/book-open-bookmark.png') + '" title="'+ _('Read') + '" alt="'+_('Read')+'" /></a>'
        t_dict['edit'] = '<a href="'+ reverse('text_detail') + '?edit='+str(t.id) + '"><img src="' + \
            static('lwt/img/icn/document--pencil.png') + '" title="'+ _('edit') + '" alt="'+_('edit')+'" /></a>'
        ##############################
        t_dict['language'] = t.language.name
        ##############################
        r = t.title
        tag_for_text = [tt.txtagtext for tt in t.texttags.all()]
        if tag_for_text: # display the tags if there are
            r += ' <span class="small">['+ ','.join(tag_for_text) + ']</span>'
        ##############################
        if t.audiouri != "":
            r += ' <img src="' + static('lwt/img/icn/speaker-volume.png') +\
                '" title="'+_("With Audio")+'" alt="'+_('With Audio')+ '/>'
        ##############################
        if t.sourceuri != "" and t.sourceuri != None:
            r += '<a href="'+ t.sourceuri + '" target="_blank"><img src="'+\
            static('lwt/img/icn/chain.png')+'" title="'+_("Link to Text Source")+'" alt="'+_("Link to Text Source")+\
            '"/></a>'
        t_dict['title_tag'] = r
        ##############################display some stats about the Texts: ############################################
        texttotalword = Words.objects.filter(owner=request.user).filter(text=t).\
                exclude(Q(isnotword=True)&Q(isCompoundword=False)).count()
        textsavedword = Words.objects.filter(owner=request.user).filter(text=t).filter(status__gt=0).\
                exclude(Q(isnotword=True)&Q(isCompoundword=False)).count()
        textsavedexpr = Words.objects.filter(owner=request.user).filter(text=t,isCompoundword=True,status__gt=0).count()
        textunknownword = texttotalword - textsavedword
        if texttotalword != 0:
            textunknownwordpercent = 100 * textunknownword//texttotalword
        else: 
            textunknownwordpercent = 0
        ############################## Total words
        r = '<span title="'+_("Total")+ '">'
        r += '<a href="'+reverse('term_list')+'?text='+ str(t.id) 
        r += '">'+ str(texttotalword)+ '</a></span>'
        t_dict['total_words'] = r
        ############################## Saved words
        r = '<span title="'+ _("Saved")+'" class="status4">'
        if textsavedword > 0:
            r += '<a href="'+reverse('term_list')+'?text='+ str(t.id) + '&status=[1,100,101]'
            r += '">'+ str(textsavedword)+ '</a>' 
            r += ' (<a href="'+reverse('term_list')+'?text='+ str(t.id) + '&status=[1,100,101]&word_compoundword=compoundword'
            r += '">' + str(textsavedexpr) +'</a>)'
        else:
            r += '0'
        r += '</span>'
        t_dict['saved_words'] = r
        ############################## Unknown Words
        r = '<span title="'+_("Unknown")+'" class="status0">'
        r += '<a href="'+reverse('term_list')+'?text='+ str(t.id) + '&status=[0]'\
        '">'+ str(textunknownword)+ '</a></span>'
        t_dict['unknown_words'] = r
        ############################## Uknown words percent
        r = '<span title="'+_("Unknown (%)")+'" class="status0">'
        r += '<a href="'+reverse('term_list')+'?text='+ str(t.id) + '&status=0'\
        '">'+ str(textunknownwordpercent)+ '</a></span>'
        t_dict['unknown_words_pc'] = r
            
        ##############################
        if t.lastopentime:
            r = '<span class="hidden">'+ str(t.lastopentime.timestamp()) + '</span>' +\
                                    str(timesince.timesince(t.lastopentime))
        else:
            r = _('never') 
        t_dict['lastopentime'] = r
        ##############################

        data.append(t_dict)
            
    return JsonResponse({'total': total, 'rows': data}, safe=False)


''' all of the Texts list in the selected langugage'''
@login_required
@nolang_redirect
def text_list(request):
    ######################################## Get Settings ##################################################################
    # get currentlang_id from cookie, else from database
    currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)
    currentlang_name = getter_settings_cookie_else_db('currentlang_name',request)

    # Filtering when we first open the page. there's another filtering which is done by clicking on checkbox
    # get the cookie if set: 
    ############## cookie for LANGUAGE FILTERING ##########################################################################
    if 'lang' in request.GET.keys(): # the language_list page has a link to display the texts with specific language
        lang_filter_json = '[' + request.GET['lang'] + ']'
        setter_settings_cookie('lang_filter', lang_filter_json, request)
    else:
        lang_filter_json = getter_settings_cookie('lang_filter', request)
        if not lang_filter_json or lang_filter_json == '[]': # first time openin, default it to currentlang
            lang_filter_json = '['+ str(currentlang_id) + ']'
            setter_settings_cookie('lang_filter', lang_filter_json, request)
    lang_filter = json.loads(lang_filter_json)
    lang_filter = [int(i) for i in lang_filter]

    ############## cookie for TEXTTAG FILTERING ##########################################################################
    texttag_filter_json = getter_settings_cookie('texttag_filter', request)
    texttag_filter = [] if not texttag_filter_json else json.loads(texttag_filter_json)
    texttag_filter = [int(i) for i in texttag_filter]
    texttags = Texttags.objects.filter(owner=request.user).all().order_by('txtagtext')
    # We don´t display texttag for which there is no texts associated with
    # ... this is determined by the checkbox of language above
    #... create a zipped list of texttag with its associated languages found inside:
    # e.g: [{'tag': <Texttags: a>, 'hidden': False, 'lang': [11]},
    #       {'tag': <Texttags: annotation>, 'hidden': True, 'lang': [6, 2]}, ...}]
    texttags_list = []
    texttags_list_empty = True
    for texttag in texttags:
        # get the languages which are found associated to this texttag
        texttag_lang = Texts.objects.filter(texttags=texttag).values_list('language_id', flat=True).all()
        if set(texttag_lang).isdisjoint(set(lang_filter)): # some languages are common
            texttags_list.append({'tag':texttag, 'hidden': True, 'lang': list(texttag_lang)})
        else:
            texttags_list.append({'tag':texttag, 'hidden': False, 'lang': list(texttag_lang)})
            texttags_list_empty = False
        

    ##################################### Lastopentime filtering #############################################################
    now = timezone.now()
    possible_time = [
        {'week': [0,4], 'string':_('< 1 month ago')},
        {'week': [4,12], 'string': _('1 mo - 3 mo ago')},
        {'week': [12,24], 'string': _('3 mo - 6 mo ago')},
        {'week': [24,-1], 'string':_('> 6 months ago or never opened')}
        ]
    # cookie for TIME FILTERING
    time_filter_json = getter_settings_cookie('time_filter', request)
    time_filter = [] if not time_filter_json else json.loads(time_filter_json)
    time_filter = [json.loads(tf) for tf in time_filter]
#     time_filter = [int(i) for i in time_filter]
    # create a zipped list of texttag with its associated languages found inside:
    time_list = []
    time_list_empty = True # everything is hidden
    for pt in possible_time:
        week = pt['week']
        if week[1] == -1: # it's older than 6 months. We put also texts never opened before
            length_of_time = timedelta(weeks=week[0])
            cutout_date = now - length_of_time
            time_text_ids = list(Texts.objects.filter(owner=request.user).\
                        filter(Q(lastopentime__lte=cutout_date)|\
                                Q(lastopentime__isnull=True)).\
                              values_list('id', flat=True))
        else:
            # and for the recent cutout date:
            recent_length_of_time = timedelta(weeks=week[0])
            recent_cutout_date = now - recent_length_of_time
            recent_time_Q_filter = Q(lastopentime__lte=recent_cutout_date)
            # and for the ancient cutout date:
            ancient_length_of_time = timedelta(weeks=week[1])
            ancient_cutout_date = now - ancient_length_of_time
            ancient_time_Q_filter = Q(lastopentime__gt=ancient_cutout_date)
            time_text_ids = list(Texts.objects.filter(owner=request.user).\
                                 filter(recent_time_Q_filter&ancient_time_Q_filter).\
                                values_list('id', flat=True))
        if time_text_ids: # some languages are common
            dic = {'pt': pt, 'text_ids':time_text_ids, 'hidden': False}
            time_list.append(dic)
        else:
            dic = {'pt': pt, 'text_ids':time_text_ids, 'hidden': True}
            time_list.append(dic)
            time_list_empty = False

    # get the list of languages to display them in the drop-down menu:
    languages = Languages.objects.filter(owner=request.user).all().order_by('name')

    ##################################### Deleting a file #############################################################
    if request.GET.get('del'):
        ids_to_delete = request.GET['del']
        ids_to_delete = json.loads(ids_to_delete)
        delse_nb = 0
        deltx_nb = 0
        for text_id in ids_to_delete:
            # first delete the se with the foreignkeys
            delse = Sentences.objects.filter(owner=request.user).filter(text__id=text_id).delete()
            deltx = Texts.objects.filter(owner=request.user).get(id=text_id).delete() # then delete the text itself
            delse_nb += delse[0]
            deltx_nb += deltx[0]
        messages.add_message(request, messages.SUCCESS, str(deltx_nb) + _(' Text(s) deleted / ') + str(delse_nb) + _(' sentence(s) deleted / '))
        #update the cookie for the database_size
        set_word_database_size(request)

    ##################################### Set currentlang #############################################################
    if request.GET.get('currentlang_id'):
        lgid = request.GET.get('currentlang_id')
        setter_settings_cookie_and_db('currentlang_id', lgid, request)
        currentlang_id = int(lgid)
    
    # get the current database size:
    database_size = get_word_database_size(request)

    return render (request, 'lwt/text_list.html',
                   {
                    'languages':languages, 
                    'lang_filter':lang_filter, 'texttag_filter':texttag_filter, 
                    'time_filter':time_filter, 
                    'texttags_list': texttags_list, 'texttags_list_empty':texttags_list_empty,
                    'time_list': time_list, 'time_list_empty':time_list_empty,
                    'timezone_now': now,
                    'currentlang_id':currentlang_id,'currentlang_name':currentlang_name,
                     'database_size':database_size})

''' Editing a single text, or Creating a new text'''
@login_required
@nolang_redirect
def text_detail(request):
        
    # POST method: a new language has been created or a old one is edited, or a filter is applied
    if request.method == 'POST':
        f = TextsForm(request.POST or None)
        if f.is_valid():
            savedtext = f.save()
            # add the Owner in the texttags model (not done automatically)
            for ttag in savedtext.texttags.all():
                ttag.owner = request.user
                ttag.save()
            
            # Process the file :
            # split the text into sentences and into words and put it in Unknownwords
            splitText(request, savedtext) #  in _utilities_views

            messages.add_message(request, messages.SUCCESS, _('Text successfully added'))
            #update the cookie for the database_size
            set_word_database_size(request)

            return redirect(reverse('text_list'))
        else:
            messages.add_message(request, messages.ERROR, _('There was an error in adding this text.'))
            return render(request, 'lwt/text_detail.html', {'form':f})
    # Displaying the form to Create a new text, Edting a text:
    elif request.method == 'GET':
        # get currentlang_id from cookie, else from database
        currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)
        # ... and get the name: used for the page title:
        currentlang_name = getter_settings_cookie_else_db('currentlang_name',request)

        if 'new' in request.GET.keys():
            # must display the form for the first time:

            if int(currentlang_id) != -1:  # Put an initial value in the language dropdown menu:
                currentlang = Languages.objects.get(id=currentlang_id)
                f = TextsForm(initial = {'owner': request.user, 'language':currentlang}) # always set the owner as default request.user
            else:
                f = TextsForm(initial = {'owner': request.user}) # always set the owner as default request.user
            word_inthistext=None
            # STRING CONSTANTS:
            op = 'new'
            text_title = '' # used by edit section
        if 'edit' in request.GET.keys():
            text_id = request.GET['edit']
            text = Texts.objects.all().get(id=text_id)
            f = TextsForm(instance=text)
            word_inthistext = Words.objects.filter(text=text).order_by('sentence_id', 'order')
            # STRING CONSTANTS:
            op = 'edit'
            text_title = text.title # used by edit section

        f_uploaded_text = Uploaded_textForm()
        # get the list of languages to display them in the drop-down menu:
        language_selectoption = Languages.objects.values('name','id').order_by('name')
        return render(request, 'lwt/text_detail.html', {
                            'form':f, 'language_selectoption':language_selectoption,
                            'form_uploaded_text':f_uploaded_text,
                            'currentlang_id':currentlang_id,'currentlang_name':currentlang_name,
                            # inside thetext div:
                            'word_inthistext':word_inthistext,
                            # STRING CONSTANTS:
                            'op':op, 'text_title':text_title
                                                     })
        
''' called by ajax in text_detail.html to uploade a text file, process it 
to extract the text and title'''
def uploaded_text(request):
    if request.method == 'POST':
        form = Uploaded_textForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            files = form.save()
            title = files.uploaded_text.name
            title = title.split('.')[0] # myfile.txt => title = 'myfile'
            try:
                with open(files.uploaded_text.path, 'r') as f:
                    text = f.read() 
                delete_uploadedfiles(Uploaded_text)
                return HttpResponse(json.dumps({'title':title, 'text':text}))
            except UnicodeDecodeError as e: # the file contains not unicode characters
                delete_uploadedfiles(Uploaded_text)
                return HttpResponse(json.dumps({'error':'{} ("{}")'.format(gettext('Check coding of this text!'), e)}))
        else:
            delete_uploadedfiles(Uploaded_text)
            return HttpResponse(json.dumps({'error':form.errors}))

