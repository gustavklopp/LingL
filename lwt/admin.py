# Admin for Development: admin / pw: adminadmin
from django.contrib import admin
from lwt.models import Lwtgeneral
from lwt.models import Archivedtexts
from lwt.models import Archtexttags
from lwt.models import Languages
from lwt.models import Sentences
from lwt.models import Settings
from lwt.models import Tags
from lwt.models import Tags2
from lwt.models import Textitems
from lwt.models import Texttags
from lwt.models import Words
from lwt.models import Wordtags

admin.site.register(Lwtgeneral)
admin.site.register(Archivedtexts)
admin.site.register(Archtexttags)
admin.site.register(Languages)
admin.site.register(Sentences)
admin.site.register(Settings)
admin.site.register(Tags)
admin.site.register(Tags2)
admin.site.register(Textitems)
admin.site.register(Texttags)
admin.site.register(Words)
admin.site.register(Wordtags)
