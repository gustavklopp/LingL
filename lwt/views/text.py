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
from django.utils.translation import ugettext as _, ngettext
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
from lwt.constants import MAX_WORDS_DANGER


''' called by ajax (built-in function) inside bootstrap-table #text_table to fill the table'''
def load_texttable(request):
    order, sort, sort_modif, offset, offset_modif, limit, limit_modif, all_texts = requesting_get_by_table(request, Texts)

    if 'search' in request.GET.keys():
        search = request.GET['search']
        if search != '': # when deleting the previous search, ajax will send the search word ''. consider it like No filter
            all_texts = all_texts.filter(title=search)

    if not all_texts: # directly return if no texts to load!
            return JsonResponse({'total': 0, 'rows': []}, safe=False)

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
        if not t.archived: # display a choice popup if trying to read/edit an archived text
            onclick_r = 'document.location = \''+reverse('text_read',args=[t.id]) +'\';'
            onclick_e = 'document.location = \''+reverse('text_detail')+'?edit='+str(t.id)+'\';'
        else:
            onclick_r = 'warning_archive(\''+reverse('text_read',args=[t.id]) +'\');'
            onclick_e = 'warning_archive(\''+reverse('text_detail')+'?edit='+str(t.id)+'\');'
        t_dict['read'] = '<img class="btn" onclick="'+onclick_r+'" src="' + \
            static('lwt/img/icn/book-open-bookmark.png') + '" title="'+ _('Read text') + '" alt="'+_('Read')+'" />'
        t_dict['edit'] = '<img class="btn" onclick="'+onclick_e+'" src="' + \
            static('lwt/img/icn/document--pencil.png') + '" title="'+ _('edit text') + '" alt="'+_('edit')+'" />'
        ##############################
        t_dict['language'] = t.language.name
        ##############################
        r = t.title
        tag_for_text = [tt.txtagtext for tt in t.texttags.all()]
        if tag_for_text != []: # display the tags if there are
            r += ' <span class="small">['+ ','.join(tag_for_text) + ']</span>'
        ##############################
        if t.audiouri != "" and t.audiouri != None: #I use the 'or' because in the fixture demo, it's sometimes null or ''
            r += ' <img src="' + static('lwt/img/icn/speaker-volume.png') +\
                '" title="'+_("With Audio")+'" alt="'+_('With Audio')+ '"/>'
        ##############################
        if t.sourceuri != "" and t.sourceuri != None:
            r += '<a href="'+ t.sourceuri + '" target="_blank"><img src="'+\
            static('lwt/img/icn/chain.png')+'" title="'+_("Link to Text Source")+'" alt="'+_("Link to Text Source")+\
            '"/></a>'
        t_dict['title_tag'] = r
        if not t.archived:
            ##########################################################################
            #        display some statistics about the Texts:                             #
            ##########################################################################
            # Total words in this text: don't count duplicate (words written similarly)
#             texttotalword_list = Words.objects.filter(text=t).\
#                     exclude(isnotword=True).annotate(wordtext_lc=Lower('wordtext')).order_by('wordtext_lc')
#             texttotalword_list = (distinct_on(texttotalword_list, 'wordtext', case_unsensitive=True))
#             texttotalword = len(texttotalword_list)
            texttotalword = t.wordcount_distinct
                    
            # Already saved words in this text: don't count duplicate (words written similarly) 
            textsavedword_list = Words.objects.filter(Q(text=t)&Q(isnotword=False)&Q(status__gt=0)).\
                               annotate(wordtext_lc=Lower('wordtext')).\
                                                    order_by('wordtext_lc')
            textsavedword_list = (distinct_on(textsavedword_list, 'wordtext', case_unsensitive=True))
            textsavedword = len(textsavedword_list)
                            
#             textsavedword = len([wo for wo in texttotalword_list if wo.status != 0])

            textsavedexpr = Words.objects.filter(Q(text=t)&Q(isCompoundword=True)&\
                                                 Q(isnotword=True)&Q(status__gt=0)).count()
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
                r += ' ('
                if textsavedexpr != 0:
                    r += '<a href="'+reverse('term_list')+'?text='+ str(t.id) + '&status=[1,100,101]&word_compoundword=compoundword">'
                r += str(textsavedexpr)
                if textsavedexpr != 0:
                    r += '</a>'
                r += ')'
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
            '">'+ str(textunknownwordpercent)+ '%</a></span>'
            t_dict['unknown_words_pc'] = r
        else: # text is archived:
            r = '<span title="'+_('text is archived. Calculation not possible.')+'">&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;</span>'
            t_dict['total_words'] = r
            t_dict['saved_words'] = r
            t_dict['unknown_words'] = r
            t_dict['unknown_words_pc'] = r
            
        ##############################
        if t.lastopentime:
            r = '<span class="hidden">'+ str(t.lastopentime.timestamp()) + '</span>' +\
                                    str(timesince.timesince(t.lastopentime))
        else:
            r = _('never') 
        t_dict['lastopentime'] = r
        ##############################
        r = '<img class="btn" onclick="document.location = \''+reverse('text_list')+'?unarchive='+str(t.id)+'\';" title="'+_('text was archived. Click to Un-archive')+'" src="'+static('lwt/img/icn/archive-box.png')+'" />'
        t_dict['archived'] = r if t.archived else '' 

        data.append(t_dict)
            
    return JsonResponse({'total': total, 'rows': data}, safe=False)

''''the checkboxes to filter the terms. called by Ajax_text_list '''
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

''' all of the Texts list in the selected langugage'''
@login_required
@nolang_redirect
def text_list(request):
    ######################################## Get Settings ##################################################################
    # get currentlang_id from cookie, else from database
    currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)
    currentlang_name = getter_settings_cookie_else_db('currentlang_name',request)

    # Filtering when we first open the page. there's another AJAX filtering which is done by 
    # ...clicking on checkbox. We get the cookie if set: 
    ############## cookie for LANGUAGE FILTERING ##########################################################################
    if 'lang' in request.GET.keys(): # the language_list page has a link to display the texts with specific language
        lang_filter_json = '[' + request.GET['lang'] + ']'
        setter_settings_cookie('lang_filter', lang_filter_json, request)
    else:
        lang_filter_json = getter_settings_cookie('lang_filter', request)
        if not lang_filter_json or lang_filter_json == '[]': # first time openin, default it to currentlang
            lang_filter_json = '['+ str(currentlang_id) + ']'
            setter_settings_cookie('lang_filter', lang_filter_json, request)
    lang_Ids_list = json.loads(lang_filter_json)
    lang_Ids_list = [int(i) for i in lang_Ids_list]

    languages = Languages.objects.filter(owner=request.user).all().order_by('name')
    lang_textIds_list = []
    lang_textIds_set = set()
    for lang in languages:
        txts = list(Texts.objects.filter(Q(owner=request.user)&\
                                      Q(language=lang)).values_list('id', flat=True))
        lang_textIds_list.append({'lang':lang, 'txt_set':txts, 'txt_set_json':json.dumps(txts)})
        if lang.id in lang_Ids_list:
            lang_textIds_set |= set(txts)


    ############## cookie for TEXTTAG FILTERING ##########################################################################
    texttag_filter_json = getter_settings_cookie('tag_filter', request)
    texttag_filter = [] if not texttag_filter_json else json.loads(texttag_filter_json)
    texttag_filter = [int(i) for i in texttag_filter]
    texttags = Texttags.objects.filter(owner=request.user).all().order_by('txtagtext')
    # We don´t display texttag for which there is no texts associated with
    # ... this is determined by the checkbox of language above
    texttags_list_empty = True
    for texttag in texttags:
        #get the languages which are found associated to this texttag
        texttag_lang = Texts.objects.filter(texttags=texttag).values_list('language_id', flat=True).all()
        if set(texttag_lang).isdisjoint(set(lang_Ids_list)): # some languages are common
            continue
        else:
            texttags_list_empty = False
    # list of all texts having the selected texttags (whatever language or time)
    texttag_textIds_boldlist = []
    texttag_textIds_set = set()
    for ttag in texttags:
        txts = list(Texts.objects.filter(Q(owner=request.user)&Q(texttags=ttag)).values_list('id', flat=True))
        texttag_textIds_set |= set(txts)
        texttag_textIds_boldlist.append({'texttag':ttag, 'txt_set':txts, 
                                         'txt_set_json':json.dumps(txts), 'bold':False})

    ##################################### Lastopentime filtering #############################################################
    now = timezone.now()
    possible_time = [
        {'week': [0,4], 'string':_('< 1 month ago')},
        {'week': [4,12], 'string': _('1 mo - 3 mo ago')},
        {'week': [12,24], 'string': _('3 mo - 6 mo ago')},
        {'week': [24,-1], 'string':_('> 6 months ago or never opened')}
        ]
    # cookie for TIME FILTERING
    time_filter_json = getter_settings_cookie('time_filter', request) # --> ex.: str: "["[24, -1]"]"
    if time_filter_json == None: 
        # first time opening LingL: no cookie: the default is then to make it all time...
        # ... selected
        time_filter = [el['week'] for el in possible_time]
    elif time_filter_json == '[]':
        time_filter = []
    else:
        time_filter = [json.loads(tf) for tf in json.loads(time_filter_json)]
        
    # get all texts (whatever languages or texttag) with this time
    time_textIds_boldlist = []
    time_textIds_set = set()

    for pt in possible_time:
        week = pt['week']
        if week[1] == -1: # Special case for when older than 6 months. We put also texts never opened before
            length_of_time = timedelta(weeks=week[0])
            cutout_date = now - length_of_time

            # get all texts (whatever languages and texttags) with this time
            txts = list(Texts.objects.filter(Q(owner=request.user)&\
                                             Q(lastopentime__lte=cutout_date)|\
                                             Q(lastopentime__isnull=True)).\
                                     values_list('id', flat=True))
            time_textIds_set |= set(txts)
            time_textIds_boldlist.append({'time':pt, 'txt_set':txts, 
                                          'txt_set_json':json.dumps(txts), 'bold':False})
        else:
            # and for the recent cutout date:
            recent_length_of_time = timedelta(weeks=week[0])
            recent_cutout_date = now - recent_length_of_time
            recent_time_Q_filter = Q(lastopentime__lte=recent_cutout_date)
            # and for the ancient cutout date:
            ancient_length_of_time = timedelta(weeks=week[1])
            ancient_cutout_date = now - ancient_length_of_time
            ancient_time_Q_filter = Q(lastopentime__gt=ancient_cutout_date)

            # get all texts (whatever languages and texttags) with this time
            txts = list(Texts.objects.filter(owner=request.user).\
                                      filter(recent_time_Q_filter&ancient_time_Q_filter).\
                                     values_list('id', flat=True))
            time_textIds_set |= set(txts)
            time_textIds_boldlist.append({'time':pt, 'txt_set':txts, 
                                          'txt_set_json':json.dumps(txts), 'bold':False})
    
    # which items of each checkbox forms (language, texttags, time) should be displayed in bold?
    for idx, texttag in enumerate(texttag_textIds_boldlist):
        iscommonwith = False if (set(texttag['txt_set']).isdisjoint(lang_textIds_set) \
                                 or set(texttag['txt_set']).isdisjoint(time_textIds_set)) else True
        texttag_textIds_boldlist[idx]['bold'] = iscommonwith
    for idx, time in enumerate(time_textIds_boldlist):
        if texttags_list_empty: # no texttags. the texttag_textIds_set is {}
                                # so iscommonwith is always False if we don't do this condition
            iscommonwith = False if (set(time['txt_set']).isdisjoint(lang_textIds_set)) else True
        else: 
            iscommonwith = False if (set(time['txt_set']).isdisjoint(lang_textIds_set) \
                                     or set(time['txt_set']).isdisjoint(texttag_textIds_set)) else True
        time_textIds_boldlist[idx]['bold'] = iscommonwith

    ############## cookie for ARCHIVED FILTER###############################################################
    archived_filter_json = getter_settings_cookie('archived_filter', request)
    archived_filter = [] if not archived_filter_json else json.loads(archived_filter_json)
    archived_filter = [str_to_bool(i) for i in archived_filter]
    archived_textIds = list(Texts.objects.filter(Q(owner=request.user)&Q(archived=True)).values_list('id', flat=True))
    notarchived_textIds = list(Texts.objects.filter(Q(owner=request.user)&Q(archived=False)).values_list('id', flat=True))
    # display in bold or not
    nonarchived_iscommonwith = not lang_textIds_set.isdisjoint(set(notarchived_textIds))
    archived_iscommonwith = not lang_textIds_set.isdisjoint(set(archived_textIds))

    archived_textIds_boldlist = [  {'archived':False, 'txt_set':json.dumps(notarchived_textIds), 
                                        'bold':nonarchived_iscommonwith},
                                   {'archived':True, 'txt_set':json.dumps(archived_textIds), 
                                        'bold':archived_iscommonwith} ]

    ################################ Deleting or Archiving a text #####################################
    if 'del' in request.GET.keys() or 'archive' in request.GET.keys():
        if 'del' in request.GET.keys():
            op = 'deleting'
            ids_to_del_OR_archive = request.GET['del']
            # it's possible to delete text but keep the already saved words:
            is_deleting_saved_words = str_to_bool(request.GET['is_deleting_saved_words'])
        else:
            op = 'archiving'
            ids_to_del_OR_archive = request.GET['archive']
        ids_to_del_OR_archive = json.loads(ids_to_del_OR_archive)

#         delse_nb = 0
        delORarchivetxt_nb = 0
        delwo_nb = 0
        
        for text_id in ids_to_del_OR_archive:
            # Case of words unknown (status == 0): deleted, whatever the case
            delwo_nb += Words.objects.filter(Q(text_id=text_id)&Q(status=0)).delete()[0]

            # and delete also notaword (which are not compoundword):
            Words.objects.filter(Q(text_id=text_id)&Q(isnotword=True)&Q(isCompoundword=False)).delete()
            
            # Case of saved words (status != 0):
            todel_OR_toarchive_words = Words.objects.filter(owner=request.user).order_by(
                                                            'grouper_of_same_words','wordtext')
            todelete_savedwords = [] # used for bulk delete
            prev_wordtext = ''
            prev_gosw = None
            for todel_OR_toarchive_wo in todel_OR_toarchive_words:
                # don't keep same saved words written similarly
                if todel_OR_toarchive_wo.wordtext.lower() == prev_wordtext and \
                            todel_OR_toarchive_wo.grouper_of_same_words == prev_gosw:
                    todelete_savedwords.append(todel_OR_toarchive_wo.id)
                    continue
                else:
                    prev_wordtext = todel_OR_toarchive_wo.wordtext.lower()
                    prev_gosw = todel_OR_toarchive_wo.grouper_of_same_words

                # if status == 0 -> we delete the words whatever the case.
                # else:   - if it's archiving:  we keep the saved words
                #         - or: if it's deleting: we keep the saved words if the option 'is_deleting_saved_words'...
                #                           was not checked
                if op == 'deleting' and is_deleting_saved_words:
                    # delete also Grouper_of_same_words associated:
                    # maybe there isn´t (if we have make this word as a similar word to another)
                    # we want to keep words in other texts though
                    # get the grouper_of_same_words (GOSW) for this word, and if the GOSW has itself...
                    # no other Words for which it is the FK: delete it:
                    todelORtoarchivewo_gosw = todel_OR_toarchive_wo.grouper_of_same_words
                    if todelORtoarchivewo_gosw: # word has gosw, we must process it
                        count_words_for_this_gosw = Words.objects.filter(grouper_of_same_words=todelORtoarchivewo_gosw).count()
                        if count_words_for_this_gosw == 1:
                            todel_OR_toarchive_wo.grouper_of_same_words.delete()
                        else:
                            todel_OR_toarchive_wo.grouper_of_same_words = None
                    if not todel_OR_toarchive_wo.isnotword:
                        delwo_nb += 1
                    todel_OR_toarchive_wo.delete()

            # bulk delete:
            delwo_nb += Words.objects.filter(id__in=todelete_savedwords).delete()[0]

            # all sentences need to be deleted and in Words: set order and textOrder to Null
            Sentences.objects.filter(text_id=text_id).delete()
            Words.objects.filter(owner=request.user).filter(text_id=text_id).update(order=None, textOrder=None) 

            if op == 'deleting':
                # delete the text
                Texts.objects.filter(owner=request.user).filter(id=text_id).delete()  # then delete the text itself
                # the sentence will be deleted by cascade so no need to delete them manually
            else:
                Texts.objects.filter(owner=request.user).filter(id=text_id).update(archived=True)  # then archive the text itself
                todel_OR_toarchive_words.update(text=None) # unlink the text to the word


#             delse = Sentences.objects.filter(owner=request.user).filter(text__id=text_id).delete()
#             delse_nb += delse[0]

            delORarchivetxt_nb += len(ids_to_del_OR_archive)
        # display messages with the count of deleted text(s) and word(s)
        success_message = _('Deletion success : ') if op == 'deleting' else _('Archiving success : ')
        if op == 'deleting':
            delORarchivetx_message = ngettext('%(count)d text deleted.', '%(count)d texts deleted',
                                    delORarchivetxt_nb) % {'count': delORarchivetxt_nb}
        else:
            delORarchivetx_message = ngettext('%(count)d text archived.', '%(count)d texts archived',
                                    delORarchivetxt_nb) % {'count': delORarchivetxt_nb}
        delORarchivewo_message = ngettext('Database has been freed with %(count)d word.', 'Database has been freed with %(count)d words.',
                                delwo_nb) % {'count': delwo_nb}
        messages.add_message(request, messages.SUCCESS, success_message+delORarchivetx_message+' / '+delORarchivewo_message)
        #update the cookie for the database_size
        set_word_database_size(request)

    ############################## Deleting or Archiving a text #####################################
    if 'unarchive' in request.GET.keys():
        text = Texts.objects.get(id=request.GET['unarchive'])
        splitText(text)
        text.archived = False
        text.save()
        messages.add_message(request, messages.SUCCESS, _('Un-Archiving successfully completed'))

    ##################################### Set currentlang #############################################################
    if request.GET.get('currentlang_id'):
        lgid = request.GET.get('currentlang_id')
        setter_settings_cookie_and_db('currentlang_id', lgid, request)
        currentlang_id = int(lgid)
    
    # get the current database size:
    database_size = get_word_database_size(request)

    return render (request, 'lwt/text_list.html',
                   {'lang_filter':lang_Ids_list,'lang_textIds_list':lang_textIds_list, 
                    'time_filter':time_filter,'time_textIds_boldlist':time_textIds_boldlist, 
                    'texttag_filter':texttag_filter, 'texttag_textIds_boldlist':texttag_textIds_boldlist,
                    'archived_filter':archived_filter, 'archived_textIds_boldlist':archived_textIds_boldlist,
                    
                    'languages':languages, 'timezone_now': now,
                    'currentlang_id':currentlang_id,'currentlang_name':currentlang_name,
                    'database_size':database_size})

''' Editing a single text, or Creating a new text'''
@login_required
@nolang_redirect
def text_detail(request):
        
    # POST method: a new text has been created or a old one is edited
    # Triggered by the "Submit" button at the end of the text_detail page
    if request.method == 'POST':
        f = TextsForm(request.user, request.POST or None)
        if f.is_valid():
            if 'new' in request.GET.keys():
                # I need to manually add all the fields, I don't know why??? Bug???
                savedtext = f.save(commit=False)
                savedtext.language = f.cleaned_data['language']
                savedtext.owner = request.user
                savedtext.title = f.cleaned_data['title']
                savedtext.text = f.cleaned_data['text']
                savedtext.annotatedtext = f.cleaned_data['annotatedtext']
                savedtext.audiouri = f.cleaned_data['audiouri']
                savedtext.sourceuri = f.cleaned_data['sourceuri']
                savedtext.save()
                txtagtext_list = [] if f.data["texttags"] == '' else f.data['texttags'].split(',')
                savedtext.texttags.exclude(txtagtext__in=txtagtext_list).delete() #first, remove non existent tags
                for txtagtext in txtagtext_list:
                    texttag = Texttags.objects.get_or_create(owner=request.user, txtagtext=txtagtext)[0]
                    savedtext.texttags.add(texttag)
                savedtext.save()
                # Process the file :
                # split the text into sentences and into words and put it in Unknownwords
                splitText(savedtext) #  in _utilities_views

                ###################### Calculate how many words are for this language: Display a warning if too many words: ####################
                total_words = Words.objects.filter(owner=request.user).count()
                if total_words > MAX_WORDS_DANGER:
                    messages.add_message(request, messages.WARNING, 
                            _('With this additional text, you\'ve got now ') + str(total_words) +\
                             _(' words for ') + savedtext.language.name + \
                            _('. This could slow the program a lot. Please consider archiving or deleting some texts.'))
                text_id = savedtext.id
            else:
                savedtext = f.save(commit=False)
                # the field 'created_date' isn't copied in the model because it's an 'auto_add=True'
                # ... do it manually:
                savedtext.created_date = f.data['created_date']
                text_id = int(request.GET['edit'])
                savedtext.id = text_id # Without doing this, modelform is creating a new object, strangely...
                savedtext.save()

            # add the Owner in the texttags model (not done automatically)
            for ttag in savedtext.texttags.all():
                ttag.owner = request.user
                ttag.save()

            if 'new' in request.GET.keys():
                messages.add_message(request, messages.SUCCESS, _('Text successfully added'))
            else:
                messages.add_message(request, messages.SUCCESS, _('Text successfully modified'))
            #update the cookie for the database_size
            set_word_database_size(request)
            if 'save_read' in f.data.keys(): # clicking on button "save and read"
                return redirect(reverse('text_read', args=(text_id,)))
            else:
                return redirect(reverse('text_list'))

        else: # errors processing
            # get the current database size:
            database_size = get_word_database_size(request)

            f = TextsForm(request.user, request.POST)
            if 'new' in request.GET.keys():
                messages.add_message(request, messages.ERROR, _('There was an error in adding this text.'))
            else:
                messages.add_message(request, messages.ERROR, _('There was an error in modifying this text.'))
            return render(request, 'lwt/text_list.html', {'database_size':database_size})

    # Displaying the form to Create a new text, or Delete/Edit a word or Insert a Word:
    # (for the edit part: triggered by the submit in the tooltip)
    elif request.method == 'GET':
        # get currentlang_id from cookie, else from database
        currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)
        # ... and get the name: used for the page title:
        currentlang_name = getter_settings_cookie_else_db('currentlang_name',request)

        if 'new' in request.GET.keys():
            # must display the form for the first time:

            currentlang = Languages.objects.get(id=currentlang_id)
            f = TextsForm(request.user, initial = {'owner': request.user, 'language':currentlang}) 

            word_inthistext=None
            # STRING CONSTANTS:
            op = 'new'
            text_title = '' # used by edit section
            created_date = None
            text_id = None

        # editing a word
        elif 'word_edit' in request.GET.keys():
            wo_id = request.GET['wo_id'] # where is the word edited
            wo_wordtext = request.GET['word_edit'] # with what will the word be replace
            deleted_or_edited_word = Words.objects.get(id=wo_id)
            deleted_or_edited_word.wordtext = wo_wordtext
            deleted_or_edited_word.save()
            text = Words.objects.get(id=wo_id).text
        
        elif 'word_delete' in request.GET.keys():
            wo_id = request.GET['word_delete']
            deleted_or_edited_word = Words.objects.get(id=wo_id)
            wo_wordtext = deleted_or_edited_word.wordtext # used to update the wordcound of text
            text_id = deleted_or_edited_word.text.id
            deleted_or_edited_word.delete()
            text = Texts.objects.get(id=text_id)
            
        # inserting a word
        elif 'word_insert' in request.GET.keys():
            wo_id = request.GET['wo_id'] # where to insert the word
            wo_wordtext = request.GET['word_insert'] # what word will be inserted
            previous_space = Words.objects.get(id=wo_id)
            text = previous_space.text

            # insert the new word:
            new_word = Words()
            new_word.order = previous_space.order +1
            new_word.textOrder = previous_space.textOrder +1
            # copy all the rests
            new_word.wordtext = wo_wordtext
            new_word.isnotword = False
            new_word.owner = previous_space.owner
            new_word.language = previous_space.language
            new_word.sentence = previous_space.sentence
            new_word.text = previous_space.text
            new_word.created_date = timezone.now()

            # we insert a space also, after the new word:
            new_space = Words()
            new_space.order = previous_space.order +2
            new_space.textOrder = previous_space.textOrder +2
            new_space.wordtext = previous_space.wordtext
            new_space.isnotword = True
            new_space.owner = previous_space.owner
            new_space.language = previous_space.language
            new_space.sentence = previous_space.sentence
            new_space.text = previous_space.text
            new_space.created_date = timezone.now()

            # shift all the order and textOrder fields of the next words by 2 (we begin the shift by the last one)
            words_to_update = Words.objects.filter(Q(owner=request.user)&\
                                                   Q(text=new_space.text)&\
                                                   Q(textOrder__gt=new_space.textOrder)).order_by('-textOrder')
            for word_to_update in words_to_update:
                word_to_update.textOrder += 2
                # if it's in the same sentence, update also the 'order' field
                if word_to_update.sentence == new_space.sentence:
                    word_to_update.order += 2
            Words.objects.bulk_update(words_to_update, ['order','textOrder'])

            # we save only at the end because Unique constraint on 'textOrder' for Words
            new_word.save()
            new_space.save()

        # when deleting and inserting a word, update the wordcount and wordcound_distinct of the text
        elif 'word_delete' in request.GET.keys() or 'word_insert' in request.GET.keys():
            similarwordtext_count = Words.objects.filter(Q(text=text)&\
                                            Q(wordtext__iexact=wo_wordtext)).count()
            if 'word_insert' in request.GET.keys():
                text.wordcount += 1
                if similarwordtext_count > 1: # >1 because we have already inserted the word
                    text.wordcount_distinct += 1
            if 'word_delete' in request.GET.keys():
                text.wordcount -= 1
                if similarwordtext_count > 0: # >0 because we have already deleted the word
                    text.wordcount_distinct -= 1

        # displaying the editable text
        elif 'edit' in request.GET.keys():
            text_id = request.GET['edit']
            text = Texts.objects.get(id=text_id)
        
        # the field 'text' in Text must be changed also, and the sentence where this word is
        if 'word_delete' in request.GET.keys() or 'word_edit' in request.GET.keys() or \
                'word_edit' in request.GET.keys():
            # updating the field 'text' in Text
            allwords_in_this_text = Words.objects.filter(text=text)
            text_text = ''.join(list(allwords_in_this_text.values_list('wordtext', flat=True)))
            text.text = text_text
            text.save()
            # updating the field 'sentencetext' in Sentence
            allwords_in_this_sentence = allwords_in_this_text.filter(sentence=deleted_or_edited_word.sentence)
            sentence_sentencetext = ''.join(list(allwords_in_this_sentence.values_list('wordtext', flat=True)))
            Sentences.objects.filter(id=deleted_or_edited_word.sentence.id).update(sentencetext=sentence_sentencetext)

        # common for edit/delete a word or display the editable text
        if 'new' not in request.GET.keys(): 
            f = TextsForm(request.user, instance=text)
            word_inthistext = Words.objects.filter(text=text).order_by('sentence_id', 'order')
            # STRING CONSTANTS:
            op = 'edit'
            text_title = text.title # used by edit section
            created_date = text.created_date
            text_id = text.id


        f_uploaded_text = Uploaded_textForm()

        # get the current database size:
        database_size = get_word_database_size(request)

        # get the list of languages to display them in the drop-down menu:
        language_selectoption = Languages.objects.filter(owner=request.user).values('name','id').order_by('name')

        return render(request, 'lwt/text_detail.html', {
                            'form':f, 'language_selectoption':language_selectoption,
                            'form_uploaded_text':f_uploaded_text,
                            'currentlang_id':currentlang_id,'currentlang_name':currentlang_name,
                            # inside thetext div:
                            'word_inthistext':word_inthistext,
                            # STRING CONSTANTS:
                            'op':op, 'text_title':text_title, 'text_id': text_id,
                            'created_date':created_date,
                            'database_size':database_size
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
                with open(files.uploaded_text.path, encoding="utf8", 'r') as f:
                    text = f.read() 
                delete_uploadedfiles(files.uploaded_text.path, request.user)
                return HttpResponse(json.dumps({'title':title, 'text':text}))
            except UnicodeDecodeError as e: # the file contains not unicode characters
                delete_uploadedfiles(files.uploaded_text.path, request.user)
                return HttpResponse(json.dumps({'error':'{} ("{}")'.format(_('Check coding of this text!'), e)}))
        else:
            delete_uploadedfiles(files.uploaded_text.path, request.user)
            return HttpResponse(json.dumps({'error':form.errors}))

