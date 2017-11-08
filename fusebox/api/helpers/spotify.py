from api.models import Track, Artist
from api.services import get_spotify
import logging


class SpotifyHelper(object):
    @staticmethod
    def current_playing_track():
        client = get_spotify()
        logger = logging.getLogger(__name__)
        try:
            track_details = client._get("me/player")
        except Exception as e:
            logger.error("Failed to retrieve details about current playing song: " + str(e))
            track_details = None

        if track_details:
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
        else:
            track = None

        return track, track_details
