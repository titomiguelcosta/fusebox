from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^playing$', views.playing, name='playing'),
    url(r'^challenge', views.slack_listener, name='slack_listener'),
    url(r'^lex', views.lex, name='lex'),
]