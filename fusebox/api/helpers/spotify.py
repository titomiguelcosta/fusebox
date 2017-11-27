from api.models import Track, Artist, Played
from api.services import get_spotify
import logging
from datetime import timedelta
from django.utils import timezone


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
