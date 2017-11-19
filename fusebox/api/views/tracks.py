from api.models import Played, Track
from api.services import get_spotify
from api.formatter import SlackFormatter
from api.helpers.spotify import SpotifyHelper
from api.handlers.slack import RATE_CATEGORY_LIKE
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest


@csrf_exempt
@require_http_methods(["GET", "POST"])
def playing(request: HttpRequest) -> JsonResponse:
    track, track_details, played = SpotifyHelper.current_playing_track()

    return JsonResponse(SlackFormatter.current_playing_track(track, category=RATE_CATEGORY_LIKE, played=played))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def played(request: HttpRequest) -> JsonResponse:
    try:
        played = Played.objects.order_by("-id")[0]
        response = SlackFormatter.recently_played(played.track, category=RATE_CATEGORY_LIKE, played=played)
    except IndexError:
        response = {"text": "No song has ever been played."}

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def populate(request: HttpRequest) -> JsonResponse:
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

    response = JsonResponse({"populated": len(tracks), "errors": errors})
    response.status_code = 200 if 0 == len(errors) else 500

    return response
