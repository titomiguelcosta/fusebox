from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^track/playing$', views.playing, name='tracks_playing'),
    url(r'^track/played$', views.played, name='tracks_played'),
    url(r'^tracks/populate$', views.played, name='tracks_populate'),
    url(r'^slack/subscribe', views.slack_subscribe, name='slack_subscribe'),
    url(r'^slack/unsubscribe', views.slack_unsubscribe, name='slack_unsubscribe'),
    url(r'^slack/interactive$', views.slack_interactive, name='slack_interactive'),
    url(r'^slack/notify', views.slack_notify, name='slack_notify'),
    url(r'^users/populate', views.users_populate, name='users_populate'),
    url(r'^lex$', views.lex, name='lex'),
]
