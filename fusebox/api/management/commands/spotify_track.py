from django.core.management.base import BaseCommand
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.util import oauth2
import pprint, os


class Command(BaseCommand):
    help = 'Gets details of a track'

    def add_arguments(self, parser):
        parser.add_argument('urn', nargs='+', type=str)

    def handle(self, *args, **options):
        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth=os.getenv("SPOTIFY_ACCESS_TOKEN"), client_credentials_manager=client_credentials_manager)
        #track = sp.track(options["urn"][0])
        track = sp._get("me/player/currently-playing")
        pprint.pprint(track)
