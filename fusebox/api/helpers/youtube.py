from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from api.models import Track, Video
from django.db.models import Exists, OuterRef
import logging
import os


class YouTubeHelper(object):
    VIDEO_CATEGORY_MUSIC = '10'

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = youtube = build('youtube', 'v3', developerKey=os.getenv('GOOGLE_API_KEY'))

    def search(self, q):
        try:
            response = self.client.search().list(
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

    def populate(self):
        errors = []
        limit = 10
        last_id = 0
        total = 0

        while True:
            tracks = Track.objects.filter(
                ~Exists(
                    Video.objects.filter(
                        track=OuterRef('pk')
                    )
                ),
                id__gt=last_id
            ).order_by('id')[:limit]

            for track in tracks:
                youtube_videos = self.search("%s - %s" % (track.artists_to_str, track.title))

                if len(youtube_videos) > 0:
                    for youtube_video in youtube_videos:
                        try:
                            video = Video()
                            video.track = track
                            video.source = "youtube"
                            video.description = youtube_video["snippet"]["description"]
                            video.title = youtube_video["snippet"]["title"]
                            video.channel_id = youtube_video["snippet"]["channelId"]
                            video.url = "https://www.youtube.com/watch?v=%s" % youtube_video["id"]["videoId"]
                            video.video_id = youtube_video["id"]["videoId"]
                            video.save()
                        except Exception as e:
                            errors.append(str(e))
                            continue
                else:
                    errors.append("No videos for track %s by %s" % (track.title, track.artists_to_str))

                last_id = track.id
                total += 1

            if 0 == len(tracks):
                break

        return [total, errors]
