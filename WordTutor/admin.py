from django.contrib import admin
from WordTutor.models import *
# Register your models here.

admin.site.register(userinfo)
admin.site.register(wordinfo)
# admin.site.register(bookinfo)
# admin.site.register(noteinfo)
admin.site.register(userbook)

class NoteInfoAdmin(admin.ModelAdmin):
    list_display = ["userid","notename","wordnum","finishnum","Word"]

    def Word(self,obj):
        return [wordinfo.spell for wordinfo in obj.word.all()]
    filter_horizontal = ('word',)

admin.site.register(noteinfo,NoteInfoAdmin)

class BookInfoAdmin(admin.ModelAdmin):
    list_display = ["bookname","wordnum","User","Word"]

    def User(self,obj):
        return [userinfo.username for userinfo in obj.user.all()]

    def Word(self,obj):
        return [wordinfo.spell for wordinfo in obj.word.all()]

    filter_horizontal = ('user','word')

admin.site.register(bookinfo,BookInfoAdmin)