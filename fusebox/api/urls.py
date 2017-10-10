from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^track/playing$', views.playing, name='playing'),
    url(r'^track/playing/(?P<score>\w{0,10})/rate$', views.rate, name='rate'),
    url(r'^slack/interactive$', views.slack_interactive, name='slack_interactive'),
    url(r'^challenge$', views.slack_listener, name='slack_listener'),
    url(r'^lex$', views.lex, name='lex'),
]
