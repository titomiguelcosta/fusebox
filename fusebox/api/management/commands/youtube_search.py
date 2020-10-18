from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os


class Command(BaseCommand):
    help = "Gets details of a track"

    def add_arguments(self, parser):
        parser.add_argument("q", nargs="+", type=str)

    def handle(self, *args, **options):
        q = options["q"][0]  # query term
        youtube = build('youtube', 'v3', developerKey=os.getenv('GOOGLE_API_KEY'))
        try:
            search_response = youtube.search().list(
                q=q,
                part='id,snippet',
                maxResults=3,
                type='video',
                order='relevance',
                videoEmbeddable='true',
                videoCategoryId='10'
            ).execute()
        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

        print(search_response.get('items', []))
