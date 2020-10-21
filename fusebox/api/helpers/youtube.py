from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import os


class YouTubeHelper(object):
    VIDEO_CATEGORY_MUSIC = '10'

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def search(self, q):
        youtube = build('youtube', 'v3', developerKey=os.getenv('GOOGLE_API_KEY'))
        try:
            response = youtube.search().list(
                q=q,
                part='id,snippet',
                maxResults=3,
                type='video',
                order='relevance',
                videoEmbeddable='true',
                videoCategoryId=self.VIDEO_CATEGORY_MUSIC,
            ).execute()
        except HttpError as e:
            self.logger.error('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

            return []

        # list of dictionaries
        return response.get('items', [])
