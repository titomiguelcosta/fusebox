import spotipy.util as util
from django.core.management.base import BaseCommand
from api.services import SPOTIFY_SCOPE_DEFAULT
import spotipy


class Command(BaseCommand):
    help = "Gets details of a track"

    def add_arguments(self, parser):
        parser.add_argument("username", nargs="+", type=str)

    def handle(self, *args, **options):
        username = options["username"][0]  # pixelfusion
        token = util.prompt_for_user_token(username, SPOTIFY_SCOPE_DEFAULT)
        if token:
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_saved_tracks()
            for item in results["items"]:
                track = item["track"]
                print(track["name"] + " - " + track["artists"][0]["name"])
        else:
            print("Can't get token for", username)
