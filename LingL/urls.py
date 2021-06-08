
"""LingL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog # internationalization for javascript
# 2nd party:
# from jchart.views import ChartView  # LineChart is a class inheriting from jchart.Chart
# local import
from lwt import views

""" the XXX_detail views are called with the pattern: XXX_detail/(?P<message_key>\w+)/(?P<message_val>\w+)/$
    the XXX_list views are called with the pattern: XXX_list/?keysomething=valuesomething&amp;keyother=valueother.. . 
            the list views usually fetched a POST method and so a GET method, together, sent by the detail views.
"""


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    ##############LOCAL######################################################
    url(r'^$', views.homepage, name='homepage'),
    url(r'^profile/$', views.profile, name='profile'),
    ###### LANGUAGES ########################################################
    # create a new language or edit, or other options...:
    url(r'^language_detail/$',views.language_detail,name='language_detail'),
    # List of all languages. It is the target page after saving a new language/edit an exsting one also:
    url(r'^language_list/$',views.language_list, name='language_list'),
    url(r'^fill_language_detail/$',views.fill_language_detail,name='fill_language_detail'),

    ###### TEXTS ############################################################
    # read, test, print and improvedAnnotedText 
    url(r'^text_detail/$', views.text_detail, name='text_detail'),
    url(r'^uploaded_text/$', views.uploaded_text, name='uploaded_text'),

    # List of texts:
    url(r'^text_list/$',views.text_list, name='text_list'),
    url(r'^load_texttable/$',views.load_texttable, name='load_texttable'),
    url(r'^textlist_filter/$',views.textlist_filter, name='textlist_filter'),


    ####### TERMS ###########################################################
    # create, edit a term:
    # these 2 urls are called by AJAX (display to create a term and display dictionary webpage):
    url(r'^termform/(?P<message_key>\w+)/(?P<message_val>\w+)/$',views.termform,name='termform'),
    url(r'^termform/$',views.termform,name='termform'),
#     url(r'termform_new_or_edit/$',views.termform_new_or_edit,name='termform_new_or_edit'),
#     url(r'^show_sentence/$',views.show_sentence,name='show_sentence'),
    # searching for similar word and then create the link with the original word
    url(r'^search_possiblesimilarword/$',views.search_possiblesimilarword,name='search_possiblesimilarword'),
    url(r'^search_possiblesimilarCompoundword/$',views.search_possiblesimilarCompoundword,name='search_possiblesimilarCompoundword'),
    url(r'^create_or_del_similarword/$',views.create_or_del_similarword,name='create_or_del_similarword'),
    url(r'^submit_termformSearchbox/$',views.submit_termformSearchbox,name='submit_termformSearchbox'),

    url(r'^text_read/(?P<text_id>\w+)/$', views.text_read, name='text_read'),
    url(r'^dictwebpage/$',views.dictwebpage,name='dictwebpage'), # when it's the callback of AJAX (when clicking on word in text_read, it's at the oring ot the domain strangely...
    url(r'dictwebpage/$',views.dictwebpage,name='dictwebpage'), # no '^' because text_read calls it to display the webpage
    url(r'^update_show_compoundword/$',views.update_show_compoundword,name='toggle_show_compoundword'),
    
    # AJAX text_read iknowall
    url(r'^iknowall/$', views.iknowall, name='iknowall'),
    
    # List of the words:
    url(r'^term_list/$',views.term_list,name='term_list'),
    url(r'^load_wordtable/$',views.load_wordtable,name='load_wordtable'),
    url(r'^termlist_filter/$',views.termlist_filter,name='termlist_filter'),

    # Used for export2anki:
    url(r'^export2anki/$',views.term_list,name='export2anki'),
    url(r'^export2anki_exporter/$',views.export2anki_exporter,name='export2anki_exporter'),
    url(r'^select_rows/$',views.select_rows ,name='select_rows'),

    # Used for selectivebackup:
    url(r'^selectivebackup/$',views.term_list,name='selectivebackup'),
    url(r'^selectivebackup_exporter/$',views.selectivebackup_exporter,name='selectivebackup_exporter'),

    url(r'^statistics/$',views.statistics,name='statistics'),
    url(r'^statistics/pie_chart/(?P<language_id>\w+)/$', views.pie_chart, name='pie_chart'),
    url(r'^statistics/pie_chart/$', views.pie_chart, name='pie_chart'),
    url(r'^statistics/line_chart/(?P<language_id>\w+)/(?P<is_cumulative>\d)/$', views.line_chart, name='line_chart'),
    url(r'^statistics/line_chart/$', views.line_chart, name='line_chart'),
    
    url(r'^backuprestore/$',views.backuprestore,name='backuprestore'),
    
    #####################THIRD PARTY ########################################
    url(r'^tags_input/', include(('tags_input.urls','tags_input'), namespace='tags_input')), # used for tagging, like in "text_detail"
    url(r'^accounts/', include('allauth.urls')), # used by django-allauth

    #####################INTERNATIONALIZATION FOR JAVASCRIPT#################
   url(r'^jsi18n/lwt/$', JavaScriptCatalog.as_view(packages=['lwt']), name='javascript-catalog'), 

    # keyboard shortcuts, controls and other helps:
    url(r'^helppage/$',views.helppage, name='helppage'),
]

##################### UPLOADED RESTORE FILE    ##############################
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # used by django-allauth