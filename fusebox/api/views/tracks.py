from api.models import Played, Track
from api.helpers.spotify import SpotifyHelper
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
def queue(request: HttpRequest) -> JsonResponse:
    handler = import_string("api.handlers.slack.queue")

    return handler(request)


@protected
@csrf_exempt
@require_http_methods(["GET", "POST"])
def dequeue(request: HttpRequest) -> JsonResponse:
    handler = import_string("api.handlers.slack.dequeue")

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
    [tracks, errors] = SpotifyHelper.populate()

    response = JsonResponse({"populated": len(tracks), "errors": errors})
    response.status_code = 200 if 0 == len(errors) else 500

    return response
