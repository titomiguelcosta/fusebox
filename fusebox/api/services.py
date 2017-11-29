import os
import spotipy
from api.models import Configuration
from spotipy.oauth2 import SpotifyOAuth
import json

SPOTIFY_SCOPE_DEFAULT = "user-read-recently-played user-read-currently-playing user-top-read " \
                        "user-library-read user-follow-read playlist-read-private user-read-playback-state" \
                        "playlist-modify-private"


def get_spotify(scope=None):
    oauth = SpotifyToken(
        os.getenv("SPOTIPY_CLIENT_ID"),
        os.getenv("SPOTIPY_CLIENT_SECRET"),
        os.getenv("SPOTIPY_REDIRECT_URI"),
        cache_path=None,
        scope=SPOTIFY_SCOPE_DEFAULT if scope is None else scope
    )
    access_token = str(oauth.get_cached_token()["access_token"])
    client = spotipy.Spotify(auth=access_token)

    return client


class SpotifyToken(SpotifyOAuth):
    def get_cached_token(self):
        """
        Gets a cached auth token
        :return:
        """
        token_info = self._get_token_info()

        # if scopes don't match, then bail
        if not token_info or 'scope' not in token_info or not self._is_scope_subset(self.scope, token_info['scope']):
            return None

        if self._is_token_expired(token_info):
            token_info = self.refresh_access_token(token_info['refresh_token'])

        return token_info

    def _get_token_info(self):
        try:
            config = Configuration.objects.get(name="SPOTIFY_OAUTH")

            value = json.loads(config.value)
        except Configuration.DoesNotExist:
            value = None

        return value

    def _save_token_info(self, token_info):
        try:
            config = Configuration.objects.get(name="SPOTIFY_OAUTH")
            config.value = json.dumps(token_info)
            config.save()
        except Configuration.DoesNotExist:
            self._warn("couldn't write token cache.")
