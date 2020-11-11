from api.models import Played, Track, Rate, Video
from api.helpers.spotify import SpotifyHelper
from api.helpers.auth import protected
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.utils.module_loading import import_string
from django.utils import timezone
from django.forms.models import model_to_dict
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
import csv


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
    auth = JWTAuthentication()

    try:
        user = auth.get_user(auth.get_validated_token(auth.get_raw_token(auth.get_header(request))))
    except:
        return JsonResponse({'error': 'not authenticated'}, status=403)

    data = json.loads(request.body)

    track = Track.objects.get(pk=id)
    score = data['score'] if 'score' in data else 0
    category = data['category'] if 'category' in data else "like"
    try:
        rate = Rate.objects.get(user=user, track=track)
    except Rate.DoesNotExist:
        rate = Rate()

    if track and score >= 0:
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


@csrf_exempt
@require_http_methods(["GET"])
def details(request: HttpRequest, id: int) -> JsonResponse:
    auth = JWTAuthentication()

    try:
        user = auth.get_user(auth.get_validated_token(auth.get_raw_token(auth.get_header(request))))
    except:
        return JsonResponse({'error': 'not authenticated'}, status=403)

    try:
        track = Track.objects.get(pk=id)

        data = model_to_dict(track, exclude=['artists'])
        data['artists'] = [model_to_dict(artist, exclude=['spotify_id']) for artist in track.artists.all()[::1]]

        try:
            rate = Rate.objects.get(user=user, track=track)
            data['rate'] = {'score': rate.score}
        except Rate.DoesNotExist:
            data['rate'] = {'score': None}

        videos = Video.objects.filter(track=track)

        data['videos'] = [model_to_dict(video, exclude=['track']) for video in videos]

        response = JsonResponse(data, status=200)
    except Track.DoesNotExist:
        response = JsonResponse({'error': 'invalid track'}, status=400)

    return response


@csrf_exempt
@require_http_methods(["GET"])
def dump(request: HttpRequest) -> HttpResponse:
    auth = JWTAuthentication()

    try:
        user = auth.get_user(auth.get_validated_token(auth.get_raw_token(auth.get_header(request))))
    except:
        return JsonResponse({'error': 'not authenticated'}, status=401)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fusebox.csv"'

    fieldnames = [
        "id", "artist", "album", "title", "danceability", "energy", "loudness",
        "speechiness", "acousticness", "instrumentalness", "liveness",
        "valence", "tempo", "duration_ms", "num_played", "rate"
    ]
    tracks = Track.objects.raw(
        f'''select
                t.*, avg(r.score) as rate, count(distinct p.id) as num_played
            from api_track t
            inner join api_played p on t.id = p.track_id
            inner join api_rate r on r.track_id = t.id and r.user_id = {user.id}
            group by t.id'''
    )

    writer = csv.writer(response)
    writer.writerow(fieldnames)

    for track in tracks:
        writer.writerow([
            track.spotify_id,
            track.artists_to_str,
            track.album,
            track.title,
            track.danceability,
            track.energy,
            track.loudness,
            track.speechiness,
            track.acousticness,
            track.instrumentalness,
            track.liveness,
            track.valence,
            track.tempo,
            track.duration_ms,
            track.num_played,
            track.rate
        ])

    return response
