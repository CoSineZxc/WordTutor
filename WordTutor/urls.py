from django.urls import re_path, path
from WordTutor import views

urlpatterns = [
    re_path(r'^register/$', views.register),
    re_path(r'^login/$', views.firstpage),
    re_path(r'^homepage/$', views.homepage),
    re_path(r'^sethomepage/$', views.sethomepage),
    re_path(r'^vocabubook/$', views.vocabubook),
    re_path(r'^vocabunote/$', views.vocabunote),
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
    re_path(r'^.*$', views.firstpage),
]
