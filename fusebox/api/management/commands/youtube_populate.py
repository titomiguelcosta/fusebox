from django.core.management.base import BaseCommand
from api.helpers.youtube import YouTubeHelper


class Command(BaseCommand):
    help = "Populate youtube videos for tracks"

    def handle(self, *args, **options):
        [total, errors] = YouTubeHelper().populate()
        print("Poulated %d tracks with errors: %s" % (total, ', '.join(errors)))
