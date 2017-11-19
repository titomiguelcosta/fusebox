from django.conf.urls import url

from .views import generic, tracks, slack, users

urlpatterns = [
    url(r'^$', generic.index, name='index'),
    url(r'^proxy$', generic.proxy, name='proxy'),
    url(r'^tracks/playing$', tracks.playing, name='tracks_playing'),
    url(r'^tracks/played$', tracks.played, name='tracks_played'),
    url(r'^tracks/populate$', tracks.populate, name='tracks_populate'),
    url(r'^slack/subscribe', slack.subscribe, name='slack_subscribe'),
    url(r'^slack/unsubscribe', slack.unsubscribe, name='slack_unsubscribe'),
    url(r'^slack/interactive$', slack.interactive, name='slack_interactive'),
    url(r'^slack/notify', slack.notify, name='slack_notify'),
    url(r'^users/populate', users.populate, name='users_populate'),
]
