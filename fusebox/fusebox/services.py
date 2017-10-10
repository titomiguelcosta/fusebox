import os
import spotipy
from django.conf import settings
from spotipy.oauth2 import SpotifyOAuth


def get_spotify(scope="user-library-read user-read-currently-playing"):
    oauth = SpotifyOAuth(
        os.getenv("SPOTIPY_CLIENT_ID"),
        os.getenv("SPOTIPY_CLIENT_SECRET"),
        os.getenv("SPOTIPY_REDIRECT_URI"),
        cache_path=settings.BASE_DIR + "/../.cache-" + os.getenv("SPOTIPY_USERNAME"),
        scope=scope
    )
    access_token = str(oauth.get_cached_token()["access_token"])
    client = spotipy.Spotify(auth=access_token)

    return client
