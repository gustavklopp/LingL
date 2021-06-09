# django:
from django.shortcuts import render, redirect
from django.template import context
from django.template.loader import get_template
from django.templatetags.i18n import language
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Q
# first party:
from datetime import timedelta
# second party:
# third party
# local
from lwt.models import *
from lwt.constants import STATUS_CHOICES
# helper functions:
from lwt.views._nolang_redirect_decorator import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *
from tkinter.constants import ACTIVE


'''provide a different colors for each categories'''
def get_spaced_colors(n):
    if n == 1:
        return ['0,0,0'] #black if only one color requested
    else:
        max_value = 16581375 #255**3
        interval = int(max_value / (n-1)) 
        colors = [hex(I)[2:].zfill(6) for I in range(0, max_value+1, interval)] # it's max_value-1 ...
        #... because for 2 only elements for example, the range goes from 0-> max: so only one value is erroneously created
        
        return [(str(int(i[:2], 16)) +','+\
                str(int(i[2:4], 16)) +','+\
                str(int(i[4:], 16))) for i in colors]
            
''' the bar graph by week  '''
def line_chart(request, language_id=None, is_cumulative=None):
    labels = []
    y_max = 0
    activetime_filter = -1 # no time limit by default
    
    if request.method == 'POST':
        lang_filter = json.loads(request.POST['lang_filter'])
        language_ids = [-1] if -1 in lang_filter else lang_filter

        activetime_filter = int(json.loads(request.POST['activetime_filter']))
        # we display all the languages
        if language_ids == [-1]:
            languages = Languages.objects.filter(owner=request.user).order_by('name')
        else:
            languages = Languages.objects.filter(id__in=language_ids)
    else:
        is_cumulative = int(is_cumulative)
        languages = [Languages.objects.get(id=language_id)]

    words = Words.objects.exclude(status=0).\
                    filter(owner=request.user).order_by('modified_date')
    colors = get_spaced_colors(len(languages))
    first_word = words.first()
    if not first_word: # first time opening
        return JsonResponse(data={'data':'EMPTY'})

    if activetime_filter == -1:
        first_time_all = first_word.modified_date
    else:
        first_time_all = timezone.now() - timedelta(weeks=activetime_filter)        
    langs_datasets = []
    langs_datasets_cumul = []
    langs_datasets_noncumul = []
    for idx, language in enumerate(languages):
        data_points = {'cumulative':[], 'non_cumulative': []}
        first_time = first_time_all
        words_count_cumul = 0 # used for cumulative
        prev_time = None
        while (True):
            last_time = first_time + timedelta(weeks=1)
            word_perweek_count  = words.filter(language=language).\
                        filter(Q(modified_date__gte=first_time)&Q(modified_date__lt=last_time)).count()
            data_points['non_cumulative'].append(word_perweek_count)

            words_count_cumul += word_perweek_count
            data_points['cumulative'].append(words_count_cumul)
            if idx == 0: # we use the first language to create the Y label
                if not prev_time: # first date of the Y label, we display YYYY Month.
                    labels.append(first_time.strftime('(%Y) %b-%d'))
                else:
                    if first_time.month == 1 and prev_time.month == 12:
                        labels.append(first_time.strftime('(%Y) %b-%d'))
                    else:
                        if first_time.month != prev_time.month:
                            labels.append(first_time.strftime('%b-%d'))
                        else:
                            labels.append(first_time.strftime('%d'))
                prev_time = first_time
            first_time = last_time
            if first_time > timezone.now():
                break
        y_max = data_points['cumulative'][-1] # the y-axis has the same max for 'cumulative' and 'non cumul' graphs

        if request.method == 'POST':
            datasets = {
                                    'fill':True,
                                    'backgroundColor':'rgba('+colors[idx]+',0.3)',
                                    'borderColor':'rgb('+colors[idx]+')',
                                    'label': language.name, 
                                    'data':data_points['non_cumulative'],
                                    'borderWidth': 2,
                                    }
            langs_datasets_noncumul.append(datasets)
            
            datasets = {
                                    'fill':True,
                                    'backgroundColor':'rgba('+colors[idx]+',0.3)',
                                    'borderColor':'rgb('+colors[idx]+')',
                                    'label': language.name, 
                                    'data':data_points['cumulative'],
                                    'borderWidth': 2,
                                    }
            langs_datasets_cumul.append(datasets)
            
        else:
            data_inside = data_points['cumulative'] if is_cumulative else data_points['non_cumulative']
            datasets = {
                                    'fill':True,
                                    'backgroundColor':'rgba('+colors[idx]+',0.3)',
                                    'borderColor':'rgb('+colors[idx]+')',
                                    'label': language.name, 
                                    'data':data_inside,
                                    'borderWidth': 2,
                                    }
            langs_datasets.append(datasets)
    if request.method == 'POST':
        return JsonResponse( 
                            data = {'noncumulative_data': {'cargo': {
                                                        'labels': labels,
                                                        'datasets': langs_datasets_noncumul,
                                                    },
                                                   'y_max':y_max
                                                    }
                                ,
                            'cumulative_data': {'cargo': {
                                                        'labels': labels,
                                                        'datasets': langs_datasets_cumul,
                                                    },
                                                   'y_max':y_max
                                                    }
                            }
                        )
    else:
        return JsonResponse( data= {'cargo': {
                                        'labels': labels,
                                        'datasets': langs_datasets,
    #                                     'borderWidth': 2,
                                    },
                                    'y_max':y_max
                                    }
                        )


'''the Pie graph '''
def pie_chart(request, language_id=None):
#     labels = []
    data = []
    
    colors = ['#ADDFFF', '#F5B8A9', '#F8F8F8', '#CCCCCC']

    if request.method == 'POST':
        lang_filter = json.loads(request.POST['lang_filter'])
        language_ids = [-1] if -1 in lang_filter else lang_filter

        # we display all the languages
        if language_ids == [-1]:
            languages = Languages.objects.filter(owner=request.user).order_by('name')
            filter_args = Q()
        else:
            languages = Languages.objects.filter(id__in=language_ids)
            filter_args = Q(language_id__in=language_ids)
    else:
        languages = [Languages.objects.get(id=language_id)]
        filter_args = Q(language_id=language_id)

    title = _('Statuses of words for : ') + ', '.join([lang.name for lang in languages])
    words = Words.objects.exclude(Q(isnotword=True)&Q(isCompoundword=False)).\
                        filter(filter_args).order_by('status')

    labels = [STATUS_CHOICES[i]['name'] for i in STATUS_CHOICES]
    for status in STATUS_CHOICES:
        if status == 1:
            status_words_count = words.filter(Q(status__gte=1)&Q(status__lt=100)).count()
        else:
            status_words_count = words.filter(status=status).count()
        data.append(status_words_count)
    return JsonResponse(data={
                                'labels': labels,
                                'data': data,
                                'color' : colors,
                                'title': title
                            })

@login_required
@nolang_redirect
def statistics(request):
    ######################################## Get Settings ##################################################################
    # get currentlang_id from cookie, else from database
    currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)
    # get the list of languages for filtering:
    filterlangs = Languages.objects.filter(owner=request.user).order_by('name')
        
    # get the current database size:
    database_size = get_word_database_size(request)

    ########### Time filtering ###########################

    return render(request, 'lwt/statistics.html',{
        'filterlangs':filterlangs, 'currentlang_id':currentlang_id,
         'database_size':database_size
        })

