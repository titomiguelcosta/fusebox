from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from api.helpers.youtube import YouTubeHelper


class Command(BaseCommand):
    help = "Gets details of a track"

    def add_arguments(self, parser):
        parser.add_argument("q", nargs="+", type=str)

    def handle(self, *args, **options):
        q = options["q"][0]  # query term

        results = YouTubeHelper().search(q)

        print(results)
