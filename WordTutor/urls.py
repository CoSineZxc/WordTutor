from django.urls import re_path
from WordTutor import views

urlpatterns = [
    re_path(r'register', views.register),
    re_path(r'login',views.login),
    re_path(r'homepage',views.homepage),
    re_path(r'vocabubook',views.vocabubook),
    re_path(r'vocabunote',views.vocabunote),
    re_path(r'.*', views.login),
]
