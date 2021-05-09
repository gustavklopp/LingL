# Admin for Development: admin / pw: adminadmin
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
# from lwt.models import Lwtgeneral
from lwt.models import *

# admin.site.register(Lwtgeneral)
# admin.site.register(Archtexttags)
admin.site.register(Languages)
admin.site.register(Sentences)
admin.site.register(Texts)
admin.site.register(Words)
admin.site.register(Wordtags)
admin.site.register(Texttags)
admin.site.register(Grouper_of_same_words)


# Register out own model admin, based on the default UserAdmin
class MyUserAdmin(UserAdmin):
    class Meta:
        model: MyUser
        fields: '__all__'

admin.site.register(MyUser, MyUserAdmin)
