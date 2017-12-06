from django.conf import urls
from . import views

urlpatterns = [
    urls.url(r'^autocomplete/(?P<app>\w+)/(?P<model>\w+)/(?P<fields>[\w-]+)/$',
             views.autocomplete, name='autocomplete'),
]

