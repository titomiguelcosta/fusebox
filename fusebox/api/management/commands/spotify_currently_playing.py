from django.core.management.base import BaseCommand
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from django.conf import settings
from api.models import Track, Played
from django.utils import timezone


class Command(BaseCommand):
    help = 'Gets details of the current playing track'

    def handle(self, *args, **options):
        oauth = SpotifyOAuth(
            os.getenv("SPOTIPY_CLIENT_ID"),
            os.getenv("SPOTIPY_CLIENT_SECRET"),
            os.getenv("SPOTIPY_REDIRECT_URI"),
            cache_path=settings.BASE_DIR+"/../.cache-"+os.getenv("SPOTIPY_USERNAME"),
            scope="user-library-read user-read-currently-playing"
        )
        access_token = str(oauth.get_cached_token()["access_token"])
        sp = spotipy.Spotify(auth=access_token)

        track_details = sp._get("me/player/currently-playing")
        if track_details:
            track = Track.objects.get(spotify_id=track_details["item"]["uri"])
            if not track:
                track = Track()
                track.spotify_id = track_details["item"]["uri"]
                track.title = track_details["item"]["name"]
                track.save()

            played = Played()
            played.track = track
            played.on = timezone.now()
            played.save()
            print("Playing track '%s'." % track.title)
        else:
            print("Nothing playing at the moment.")
