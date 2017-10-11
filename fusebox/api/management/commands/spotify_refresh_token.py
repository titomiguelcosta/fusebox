from django.core.management.base import BaseCommand
from api.services import SpotifyToken
import os


class Command(BaseCommand):
    help = 'Refresh oauth token for spotify'

    def handle(self, *args, **options):
        oauth = SpotifyToken(
            os.getenv("SPOTIPY_CLIENT_ID"),
            os.getenv("SPOTIPY_CLIENT_SECRET"),
            os.getenv("SPOTIPY_REDIRECT_URI"),
            cache_path=None,
            scope="user-library-read user-read-currently-playing"
        )
        oauth.refresh_access_token(oauth.get_cached_token())
