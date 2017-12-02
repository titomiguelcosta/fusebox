from django.contrib import admin

from .models import Artist, Track, Played, Rate, Playlist, Configuration, PlaylistTracks

admin.site.register(Artist)
admin.site.register(Played)
admin.site.register(Track)
admin.site.register(Rate)
admin.site.register(Playlist)
admin.site.register(PlaylistTracks)
admin.site.register(Configuration)
