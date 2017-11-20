from django.contrib import admin

from .models import Artist, Track, Played, Rate

admin.site.register(Artist)
admin.site.register(Played)
admin.site.register(Track)
admin.site.register(Rate)
