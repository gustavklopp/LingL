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
from django.conf.urls import url
from django.contrib import admin
# local import
from lwt import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ##############LOCAL##############################################################################################
    url(r'^$', views.homepage, name='homepage'),

    # List of all languages. It is the target page after saving a new language/edit an exsting one also:
    url(r'^language_list/$',views.language_list,name='language_list'),
    url(r'^language_list/(?P<message_key>\w+)/(?P<message_val>\d+)$',views.language_list,name='language_list'),

    # create a new language or edit, or other options...:
    url(r'^language_detail/$',views.language_detail,name='language_detail'),
    url(r'^language_detail/(?P<message_key>\w+)/(?P<message_val>\w+)$',views.language_detail,name='language_detail'),

    # read, test, print and improvedAnnotedText 
    url(r'^text_detail/(?P<message_key>\w+)/(?P<message_val>\w+)/$', views.text_detail, name='text_detail'),
    url(r'^text_test/(?P<text_id>\d+)$', views.text_test, name='text_test'),
    url(r'^text_print/(?P<text_id>\d+)$', views.text_print, name='text_print'),
    url(r'^text_improved_print/(?P<text_id>\d+)$', views.text_improved_print, name='text_improved_print'),

    # List of homepage redirects:
    url(r'^text_list/$',views.text_list,name='text_list'),
    url(r'^text_list/(?P<lgid>\d+)$',views.text_list,name='text_list'),

    url(r'^archivedtext_list/$',views.archivedtext_list,name='archivedtext_list'),
    url(r'^archivedtext_list/(?P<lgid>\d+)$',views.archivedtext_list,name='archivedtext_list'),

    url(r'^texttag_list/$',views.texttag_list,name='texttag_list'),


    url(r'^term_list/$',views.term_list,name='term_list'),
    url(r'^term_detail/$',views.term_detail,name='term_detail'),
    url(r'^termtag_list/$',views.termtag_list,name='termtag_list'),

    url(r'^statistics/$',views.statistics,name='statistics'),
    url(r'^textcheck/$',views.textcheck,name='textcheck'),
    url(r'^longtextimport/$',views.longtextimport,name='longtextimport'),
    url(r'^termimport/$',views.termimport,name='termimport'),
    url(r'^backuprestore/$',views.backuprestore,name='backuprestore'),
    url(r'^settings/$',views.settings,name='settings'),
    url(r'^help/$',views.help,name='help'),
    url(r'^install_demo',views.install_demo,name='install_demo'),
    url(r'^do_test/(?P<lgid>\d+)$',views.do_test,name='do_test'),
    #####################THIRD PARTY ##########################################################################
    url(r'^tags_input/', include('tags_input.urls', namespace='tags_input')), # used for tagging, like in "text_detail"
    
]
