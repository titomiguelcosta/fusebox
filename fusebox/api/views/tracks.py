from api.models import Track, Played
from api.services import get_spotify
from api.helpers.auth import protected
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.utils.module_loading import import_string


@protected
@csrf_exempt
@require_http_methods(["GET", "POST"])
def playing(request: HttpRequest) -> JsonResponse:
    handler = import_string("api.handlers.slack.ratesong")

    return handler(request)


@protected
@csrf_exempt
@require_http_methods(["GET", "POST"])
def played(request: HttpRequest) -> JsonResponse:
    handler = import_string("api.handlers.slack.lastsongs")

    return handler(request)


@protected
@csrf_exempt
@require_http_methods(["GET", "POST"])
def top(request: HttpRequest) -> JsonResponse:
    tracks = Played.objects.raw(
        '''select t.*, count(p.track_id) as total from api_played p
        inner join api_track t on t.id  = p.track_id
        group by p.track_id
        order by total desc'''
    )[:10]

    data = {}
    for track in tracks:
        data["track_"+str(track.id)] = {
            "type": "integer", "value": track.total, "label": track.title
        }

    return JsonResponse(data)


@protected
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
