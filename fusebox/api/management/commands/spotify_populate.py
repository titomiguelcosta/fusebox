from django.core.management.base import BaseCommand
from api.helpers.spotify import SpotifyHelper


class Command(BaseCommand):
    help = "Populate metadata for tracks"

    def handle(self, *args, **options):
        [tracks, errors] = SpotifyHelper.populate()
        print("Poulated %d tracks with errors: %s" % (len(tracks), ', '.join(errors)))
