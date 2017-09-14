import sys
import spotipy.util as util
from django.core.management.base import BaseCommand
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pprint, os


class Command(BaseCommand):
    help = 'Gets details of a track'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)
        parser.add_argument('scope', nargs='+', type=str)

    def handle(self, *args, **options):
        username = options["username"][0]
        scope = options["scope"][0]
        token = util.prompt_for_user_token(username, scope)
        if token:
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_saved_tracks()
            for item in results['items']:
                track = item['track']
                print(track['name'] + ' - ' + track['artists'][0]['name'])
        else:
            print("Can't get token for", username)
