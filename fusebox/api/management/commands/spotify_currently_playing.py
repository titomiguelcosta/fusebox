from django.core.management.base import BaseCommand
from api.helpers.spotify import SpotifyHelper


class Command(BaseCommand):
    help = "Gets details of the current playing track"

    def handle(self, *args, **options):
        track, track_details = SpotifyHelper.current_playing_track()
        if track:
            print("Playing track: '%s' by '%s'." % (track.title, track.artists_to_str))
        else:
            print("Nothing playing at the moment.")
