from django.core.management.base import BaseCommand
from api.models import Track, Played
from django.utils import timezone
from api.services import get_spotify


class Command(BaseCommand):
    help = "Gets details of the current playing track"

    def handle(self, *args, **options):
        sp = get_spotify()
        track_details = sp._get("me/player/currently-playing")
        if track_details:
            try:
                track = Track.objects.get(spotify_id=track_details["item"]["uri"])
            except Track.DoesNotExist:
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
