from django.urls import re_path, path
from django.conf import settings
from django.conf.urls.static import static
from WordTutor import views

urlpatterns = [
    re_path(r'^register/$', views.register),
    re_path(r'^login/$', views.firstpage),
    re_path(r'^homepage/$', views.homepage),
    re_path(r'^sethomepage/$', views.sethomepage),
    re_path(r'^vocabubook/(?P<userid>[0-9]*)/$', views.vocabubook),
    re_path(r'^vocabubook/(?P<userid>[0-9]*)/(?P<book>.*)/$', views.vocabubook),
    re_path(r'^vocabunote/(?P<userid>[0-9]*)/$', views.vocabunote),
    re_path(r'^vocabunote/(?P<userid>[0-9]*)/(?P<note>.*)/$', views.vocabunote),
    re_path(r'^submit_login/$', views.login),
    re_path(r'^submit_register/$', views.register_submit),
    re_path(r'^chg_userhead/$', views.chgUserHead),
    re_path(r'^chg_username/$', views.chgUserName),
    re_path(r'^chg_userslogan/$', views.chgUserSlogan),
    re_path(r'^init_popwind_book_home/$', views.pop_home_book),
    re_path(r'^del_book_user/$', views.del_book),
    re_path(r'^add_book_user/$', views.add_book),
    re_path(r'^init_popwind_note_home/$', views.pop_home_note),
    re_path(r'^del_note_user/$', views.del_note),
    re_path(r'^add_note_user/$', views.add_note),
    re_path(r'^add_word2note/$', views.AddWord2Note),
    re_path(r'^word_next/$', views.ChgNewWord),
    re_path(r'^word_del/$', views.DelWordNote),
    re_path(r'^.*$', views.firstpage),
]
