from api.models import Track, Artist, Played, Video
from api.services import get_spotify
import logging
from datetime import timedelta
from django.utils import timezone
from api.helpers.youtube import YouTubeHelper


class SpotifyHelper(object):
    @staticmethod
    def current_playing_track():
        client = get_spotify()
        logger = logging.getLogger(__name__)
        played = None
        try:
            track_details = client._get("me/player")
        except Exception as e:
            logger.error("Failed to retrieve details about current playing song: " + str(e))
            track_details = None

        if track_details \
                and "item" in track_details \
                and "uri" in track_details["item"] \
                and "artists" in track_details["item"]:
            try:
                track = Track.objects.get(spotify_id=track_details["item"]["uri"])
            except Track.DoesNotExist:
                track = Track()
            track.title = track_details["item"]["name"]
            track.album = track_details["item"]["album"]["name"]
            track.spotify_id = track_details["item"]["uri"]
            track.url = track_details["item"]["preview_url"]
            track.save()

            for artist_details in track_details["item"]["artists"]:
                try:
                    artist = Artist.objects.get(spotify_id=artist_details["uri"])
                except Artist.DoesNotExist:
                    artist = Artist()
                artist.spotify_id = artist_details["uri"]
                artist.name = artist_details["name"]
                artist.save()

                track.artists.add(artist)
                track.save()

            # Update played song if it has not played recently
            time_threshold = timezone.now() - timedelta(minutes=120)
            try:
                played = Played.objects.filter(track=track, on__gt=time_threshold)[:1].get()
            except Played.DoesNotExist:
                played = Played()
                played.on = timezone.now()
                played.track = track
                played.save()
        else:
            track = None

        return track, track_details, played

    @staticmethod
    def populate():
        client = get_spotify()
        errors = []

        tracks = Track.objects.filter(populated=False, spotify_id__isnull=False)[:10]
        for track in tracks:
            try:
                data = client._get("audio-features/" + client._get_id("track", track.spotify_id))
            except Exception as e:
                errors.append(str(e))
                continue

            track.danceability = data["danceability"]
            track.energy = data["energy"]
            track.loudness = data["loudness"]
            track.speechiness = data["speechiness"]
            track.acousticness = data["acousticness"]
            track.instrumentalness = data["instrumentalness"]
            track.liveness = data["liveness"]
            track.valence = data["valence"]
            track.tempo = data["tempo"]
            track.duration_ms = data["duration_ms"]
            track.populated = True
            track.save()

            youtube_videos = YouTubeHelper().search("%s - %s" % (track.artists_to_str, track.title))

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

        return [tracks, errors]
