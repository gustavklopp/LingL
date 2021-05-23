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
from django.utils.translation import ugettext as _, ungettext as s_, ngettext
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
        if t.audiouri != "" and t.audiouri != None: #I use the 'or' because in the fixture demo, it's sometimes null or ''
            r += ' <img src="' + static('lwt/img/icn/speaker-volume.png') +\
                '" title="'+_("With Audio")+'" alt="'+_('With Audio')+ '"/>'
        ##############################
        if t.sourceuri != "" and t.sourceuri != None:
            r += '<a href="'+ t.sourceuri + '" target="_blank"><img src="'+\
            static('lwt/img/icn/chain.png')+'" title="'+_("Link to Text Source")+'" alt="'+_("Link to Text Source")+\
            '"/></a>'
        t_dict['title_tag'] = r
        ##############################display some stats about the Texts: ############################################
        # Total words in this text: don't count duplicate (words written similarly)
        texttotalword_list = Words.objects.filter(text=t).\
                exclude(isnotword=True).annotate(wordtext_lc=Lower('wordtext')).order_by('wordtext_lc')
        texttotalword = len(distinct_on(texttotalword_list, 'wordtext', case_unsensitive=True))
                
        # Already saved words in this text: don't count duplicate (words written similarly) 
        textsavedword = 0
        textsavedword += Words.objects.filter(Q(text=t)&Q(status__gt=0)&\
                                                Q(grouper_of_same_words=None)).count()
        gosw_textsavedwords = Words.objects.filter(Q(text=t)&Q(status__gt=0)).\
                                    exclude(grouper_of_same_words=None).order_by('grouper_of_same_words')
        distinct_gosw_textsavedwords = distinct_on(gosw_textsavedwords, 'grouper_of_same_words', case_unsensitive=False)
        textsavedword += len(distinct_gosw_textsavedwords)

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
    #... create a zipped list of texttag with its associated languages found inside:
    # e.g: [{'tag': <Texttags: a>, 'hidden': False, 'lang': [11]},
    #       {'tag': <Texttags: annotation>, 'hidden': True, 'lang': [6, 2]}, ...}]
#     texttags_list = []
    texttags_list_empty = True
    for texttag in texttags:
        #get the languages which are found associated to this texttag
        texttag_lang = Texts.objects.filter(texttags=texttag).values_list('language_id', flat=True).all()
        if set(texttag_lang).isdisjoint(set(lang_Ids_list)): # some languages are common
            continue
#         texttags_list.append({'tag':texttag, 'bold': False, 'lang': list(texttag_lang)})
        else:
#             texttags_list.append({'tag':texttag, 'bold': True, 'lang': list(texttag_lang)})
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
        
#     # create a zipped list of texttag with its associated languages found inside:
#     time_list = []
#     time_list_empty = True # everything is hidden

    # get all texts (whatever languages or texttag) with this time
    time_textIds_boldlist = []
    time_textIds_set = set()

    for pt in possible_time:
        week = pt['week']
        if week[1] == -1: # Special case for when older than 6 months. We put also texts never opened before
            length_of_time = timedelta(weeks=week[0])
            cutout_date = now - length_of_time
#             time_text_ids = list(Texts.objects.filter(owner=request.user).\
#                         filter(Q(lastopentime__lte=cutout_date)|\
#                                 Q(lastopentime__isnull=True)&\
#                                 Q(language_id__in=lang_Ids_list)).\
#                               values_list('id', flat=True))
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
#             time_text_ids = list(Texts.objects.filter(owner=request.user).\
#                                  filter(recent_time_Q_filter&ancient_time_Q_filter).\
#                                 values_list('id', flat=True))
            # get all texts (whatever languages and texttags) with this time
            txts = list(Texts.objects.filter(owner=request.user).\
                                      filter(recent_time_Q_filter&ancient_time_Q_filter).\
                                     values_list('id', flat=True))
            time_textIds_set |= set(txts)
            time_textIds_boldlist.append({'time':pt, 'txt_set':txts, 
                                          'txt_set_json':json.dumps(txts), 'bold':False})

#         if time_text_ids: # no languages selected has this time frame
#             dic = {'pt': pt, 'text_ids':time_text_ids, 'bold': False}
#         else:
#             time_list_empty = False
#             dic = {'pt': pt, 'text_ids':time_text_ids, 'bold': True}
#         time_list.append(dic)

    
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
    

    ##################################### Deleting a file #############################################################
    if request.GET.get('del'):
        ids_to_delete = request.GET['del']
        ids_to_delete = json.loads(ids_to_delete)
        # it's possible to delete text but keep the already saved words:
        delete_saved_words = str_to_bool(request.GET['delete_saved_words'])
#         delse_nb = 0
        deltx_nb = 0
        delwo_nb = 0
        for text_id in ids_to_delete:
            todelete_text = Texts.objects.filter(owner=request.user).get(id=text_id)

            # delete the words
            todelete_words = Words.objects.filter(text=todelete_text)
            toupdate_savedwords = []
            for todelete_wo in todelete_words:
                if not delete_saved_words and todelete_wo.status != 0:
                        customsentence = '' if not todelete_wo.customsentence else todelete_wo.customsentence+' / ' 
                        customsentence += todelete_wo.sentence.sentencetext
                        todelete_wo.customsentence = customsentence
                        toupdate_savedwords.append(todelete_wo)
                else:
                    # delete also Grouper_of_same_words associated:
                    # maybe there isn´t (if we have make this word as a similar word to another)
                    # we want to keep words in other texts though
                    # get the grouper_of_same_words (GOSW) for this word, and if the GOSW has itself...
                    # no other Words for which it is the FK: delete it:
                    todeletewo_gosw = todelete_wo.grouper_of_same_words
                    if todeletewo_gosw: # word has gosw, we must process it
                        count_words_for_this_gosw = Words.objects.filter(grouper_of_same_words=todeletewo_gosw).count()
                        if count_words_for_this_gosw == 1:
                            todelete_wo.grouper_of_same_words.delete()
                        else:
                            todelete_wo.grouper_of_same_words = None
                    if not todelete_wo.isnotword:
                        delwo_nb += 1
                    todelete_wo.delete()

#                     gosw_for_this_word = Grouper_of_same_words.objects.filter(id=todelete_wo.id).first()
#                     if gosw_for_this_word:
#                         gosw_for_this_word.delete()
#                         delwo_nb += 1 # else it's not a word but a space ' ', or '?', '!' etc...
#                     todelete_wo.delete()
            # bulk update:
            Words.objects.bulk_update(toupdate_savedwords, ['customsentence'])

            # delete the text
            todelete_text.delete() # then delete the text itself
            # the sentence will be deleted by cascade so no need to delete them manually
#             delse = Sentences.objects.filter(owner=request.user).filter(text__id=text_id).delete()
#             delse_nb += delse[0]

            deltx_nb += len(ids_to_delete)
        # display messages with the count of deleted text(s) and word(s)
        success_message = _('Deletion success : ')
        deltx_message = ngettext('%(count)d text deleted.', '%(count)d texts deleted',
                                deltx_nb) % {'count': deltx_nb}
        delwo_message = ngettext('%(count)d unknown word deleted.', '%(count)d unknown words deleted',
                                delwo_nb) % {'count': delwo_nb}
        messages.add_message(request, messages.SUCCESS, success_message+deltx_message+' / '+delwo_message)
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
                    'lang_filter':lang_Ids_list, 'texttag_filter':texttag_filter, 
                    'time_filter':time_filter, 
#                     'texttags_list': texttags_list, 
#                     'texttags_list_empty':texttags_list_empty,
#                     'time_list': time_list, 'time_list_empty':time_list_empty,
                    'lang_textIds_list':lang_textIds_list,
                    'texttag_textIds_boldlist':texttag_textIds_boldlist,
                    'time_textIds_boldlist':time_textIds_boldlist,
                    'timezone_now': now,
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
                savedtext = f.save()
                # Process the file :
                # split the text into sentences and into words and put it in Unknownwords
                splitText(savedtext) #  in _utilities_views
                ###################### Calculate how many words are for this language: Display a warning if too many words: ####################
                total_words_in_this_lang = Words.objects.filter(owner=request.user, 
                                                                language=savedtext.language).count()
                if total_words_in_this_lang > MAX_WORDS:
                    messages.add_message(request, messages.WARNING, 
                            _('With this additional text, you\'ve got now ') + str(total_words_in_this_lang) +\
                             _(' words for ') + savedtext.language.name + \
                            _('. This could slow the program a lot. Please consider deleting some texts.'))

            else:
                savedtext = f.save(commit=False)
                # the field 'created_date' isn't copied in the model because it's an 'auto_add=True'
                # ... do it manually:
                savedtext.created_date = f.data['created_date']
                text_id = request.GET['edit']
                savedtext.id = int(text_id) # Without doing this, modelform is creating a new object, strangely...
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
            return redirect(reverse('text_list'))

        else: # errors processing
            f = TextsForm(request.user, request.POST)
            if 'new' in request.GET.keys():
                messages.add_message(request, messages.ERROR, _('There was an error in adding this text.'))
            else:
                messages.add_message(request, messages.ERROR, _('There was an error in modifying this text.'))
            return render(request, 'lwt/text_list.html')

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

        # deleting a word
        elif 'word_delete' in request.GET.keys():
            wo_id = request.GET['word_delete']
            deleted_or_edited_word = Words.objects.get(id=wo_id)
            text_id = deleted_or_edited_word.text.id
            deleted_or_edited_word.delete()
            text = Texts.objects.get(id=text_id)

        # editing a word
        elif 'word_edit' in request.GET.keys():
            wo_id = request.GET['wo_id'] # where is the word edited
            wo_wordtext = request.GET['word_edit'] # with what will the word be replace
            deleted_or_edited_word = Words.objects.get(id=wo_id)
            deleted_or_edited_word.wordtext = wo_wordtext
            deleted_or_edited_word.save()
            text = Words.objects.get(id=wo_id).text
        
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

        # displaying the editable text
        elif 'edit' in request.GET.keys():
            text_id = request.GET['edit']
            text = Texts.objects.get(id=text_id)
        
        # the field 'text' in Text must be changed also, and the sentence where this word is
        if 'word_delete' in request.GET.keys() or \
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
                            'created_date':created_date
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
                delete_uploadedfiles(files.uploaded_text.path, request.user)
                return HttpResponse(json.dumps({'title':title, 'text':text}))
            except UnicodeDecodeError as e: # the file contains not unicode characters
                delete_uploadedfiles(files.uploaded_text.path, request.user)
                return HttpResponse(json.dumps({'error':'{} ("{}")'.format(_('Check coding of this text!'), e)}))
        else:
            delete_uploadedfiles(files.uploaded_text.path, request.user)
            return HttpResponse(json.dumps({'error':form.errors}))

