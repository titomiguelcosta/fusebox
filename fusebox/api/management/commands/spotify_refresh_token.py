from django.core.management.base import BaseCommand
from spotipy.oauth2 import SpotifyOAuth
import os


class Command(BaseCommand):
    help = 'Refresh oauth token for spotify'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        username = options["username"][0]
        oauth = SpotifyOAuth(
            os.getenv("SPOTIPY_CLIENT_ID"),
            os.getenv("SPOTIPY_CLIENT_SECRET"),
            os.getenv("SPOTIPY_REDIRECT_URI"),
            cache_path=".cache-"+username,
            scope="user-library-read user-read-currently-playing"
        )
        oauth.refresh_access_token(oauth.get_cached_token())
