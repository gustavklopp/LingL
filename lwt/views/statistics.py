
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
from jchart import Chart
from jchart.config import Axes, DataSet, rgba
# third party
# local
from lwt.models import *
from lwt.constants import STATUS_CHOICES
# helper functions:
from lwt.views._nolang_redirect_decorator import *
# helper functions:
from lwt.views._setting_cookie_db import *
from lwt.views._utilities_views import *

def get_spaced_colors(n):
    max_value = 16581375 #255**3
    interval = int(max_value / n)
    colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]
    
    return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]

class PieChart(Chart):
    chart_type = 'pie'

    def get_labels(self, **kwargs):             
        return self.labels
    
    def get_datasets(self, language_id):
        colors = ['#ADDFFF', '#F5B8A9', '#F8F8F8', '#CCCCCC']

        if language_id == 'total':
            filter_language = Q()
            label = _('Statuses of words')
        elif language_id != 'total':
            language = Languages.objects.get(id=language_id)
            filter_language = Q(language=language)
            label = _('Statuses of words for ') + language.name
        words = Words.objects.exclude(Q(isnotword=True)&Q(isCompoundword=False)).\
                            filter(filter_language).all().order_by('status')
        data = []
        self.labels = [i[1] for i in STATUS_CHOICES]
        count = 0
        for idx, el in enumerate(STATUS_CHOICES):
            if el[0] == 101:
                status_words_count = words.filter(filter_language).\
                    filter(status__gte=el[0]).count()
            else:
                status_words_count = words.filter(filter_language).\
                    filter(status__gte=el[0]).filter(status__lt=STATUS_CHOICES[idx+1][0]).count()
            data.append(status_words_count)
        return [DataSet(
                        type='pie',
                        label= label,
                        data=data,
                        backgroundColor=colors
                    )]
            
class LineChart(Chart):
    chart_type = 'bar'
    def get_labels(self, **kwargs):             
        return self.labels

    def get_datasets(self, language_id):
        if language_id == 'total':
            languages = Languages.objects.all().order_by('name')
            words = Words.objects.exclude(Q(isnotword=True)&Q(isCompoundword=False)).\
                            all().order_by('created_date')
            datasets = []
            colors = get_spaced_colors(languages.count())
            first_time_all = words.first().created_date
            self.labels = []
            for idx, language in enumerate(languages):
                data = []
                count = 0
                first_time = first_time_all
                while (first_time < timezone.now()):
                    last_time = first_time + timedelta(weeks=1)
                    time_words_count = words.filter(language=language).\
                            filter(created_date__gte=first_time).filter(created_date__lt=last_time).count()
                    data.append(time_words_count)
                    if idx == 0:
                        self.labels.append(first_time.strftime('%y-%m-%d'))
                    first_time = first_time + timedelta(weeks=1)
                datasets.append(DataSet(
                                        type='bar', 
                                        color=colors[idx],
                                        label=_('number of words created for ') + language.name, 
                                        data=data,
                                        borderWidth= 2,
                                        ))
                            
            return datasets
        else:
            language = Languages.objects.get(id=language_id)
            words = Words.objects.exclude(Q(isnotword=True)&Q(isCompoundword=False)).\
                                filter(language=language).all().order_by('created_date')
            data = []
            self.labels = []
            first_time = words.first().created_date
            count = 0
            while (first_time < timezone.now()):
                last_time = first_time + timedelta(weeks=1)
                time_words_count = words.filter(created_date__gte=first_time).filter(created_date__lt=last_time).count()
                data.append(time_words_count)
                self.labels.append(first_time.strftime('%y-%m-%d'))
                first_time = first_time + timedelta(weeks=1)
            return [DataSet(
                            type='bar',
                            label=_('number of words created for ') + language.name,
                            data=data,
                            borderWidth= 2,
                        )]


@login_required
@nolang_redirect
def statistics(request):
    ######################################## Get Settings ##################################################################
    # get currentlang_id from cookie, else from database
    currentlang_id = getter_settings_cookie_else_db('currentlang_id', request)
        # get the list of languages for filtering:
    filterlangs = Languages.objects.filter(owner=request.user).all().order_by('name')
    return render(request, 'lwt/statistics.html',{
        'filterlangs':filterlangs, 'currentlang_id':currentlang_id,
        })

