from api.models import Played, Track, Rate
from api.helpers.spotify import SpotifyHelper
from api.helpers.auth import protected
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.utils.module_loading import import_string
from django.utils import timezone
import json


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


@csrf_exempt
@require_http_methods(["POST"])
def rate(request: HttpRequest, id: int) -> JsonResponse:
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'error': 'not authenticated'}, status=403)

    data = json.loads(request.body)

    track = Track.objects.get(pk=id)
    score = data['score'] if 'score' in data else 0
    category = data['category'] if 'category' in data else "like"
    previous_rate = Rate.objects.get(user=user, track=track)

    if track and score >= 0:
        rate = previous_rate if previous_rate else Rate()
        rate.user = user
        rate.track = track
        rate.category = category
        rate.score = score
        rate.on = timezone.now()
        rate.save()

        response = JsonResponse({}, status=201)
    else:
        response = JsonResponse({'error': 'invalid track or score'}, status=400)

    return response
