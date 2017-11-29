from django.conf.urls import url

from .views import generic, tracks, slack, users

urlpatterns = [
    url(r'^$', generic.index, name='index'),
    url(r'^csv$', generic.dump, name='csv'),
    url(r'^tracks/playing$', tracks.playing, name='tracks_playing'),
    url(r'^tracks/played$', tracks.played, name='tracks_played'),
    url(r'^tracks/populate$', tracks.populate, name='tracks_populate'),
    url(r'^tracks/queue', tracks.queue, name='tracks_queue'),
    url(r'^tracks/dequeue', tracks.dequeue, name='tracks_dequeue'),
    url(r'^tracks/top', tracks.top, name='tracks_top'),
    url(r'^slack/subscribe', slack.subscribe, name='slack_subscribe'),
    url(r'^slack/unsubscribe', slack.unsubscribe, name='slack_unsubscribe'),
    url(r'^slack/interactive$', slack.interactive, name='slack_interactive'),
    url(r'^slack/notify', slack.notify, name='slack_notify'),
    url(r'^slack/proxy$', slack.proxy, name='slack_proxy'),
    url(r'^users/populate', users.populate, name='users_populate'),
]
