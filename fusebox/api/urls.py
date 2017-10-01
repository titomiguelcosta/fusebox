from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^playing$', views.playing, name='playing'),
    url(r'^challenge', views.challenge, name='challenge'),
]