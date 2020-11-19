from api.models import Track, Artist, Rate
from api.helpers.auth import jwt_auth, get_user_from_jwt_token
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.db import connection


@jwt_auth
@csrf_exempt
@require_http_methods(["GET"])
def tracks_per_artist(request: HttpRequest) -> JsonResponse:
    artists = Artist.objects.raw(
        '''select a.id, a.name, count(t.id) as total from api_artist a 
        inner join api_track_artists ap on a.id = ap.artist_id 
        inner join api_track t on ap.track_id = t.id 
        group by a.id 
        order by total desc'''
    )[:10]

    data = {"results": []}
    for artist in artists:
        data["results"].append({
            "name": artist.name,
            "tracks": artist.total,
        })

    return JsonResponse(data)


@jwt_auth
@csrf_exempt
@require_http_methods(["GET"])
def rate_per_artist(request: HttpRequest) -> JsonResponse:
    artists = Artist.objects.raw(
        '''select a.id, a.name, avg(r.score) as rate from api_artist a 
        inner join api_track_artists ap on a.id = ap.artist_id 
        inner join api_track t on ap.track_id = t.id
        inner join api_rate r on t.id = r.track_id
        group by a.id 
        order by rate desc'''
    )[:10]

    data = {"results": []}
    for artist in artists:
        data["results"].append({
            "name": artist.name,
            "rate": artist.rate,
        })

    return JsonResponse(data)


@jwt_auth
@csrf_exempt
@require_http_methods(["GET"])
def tracks_per_rate(request: HttpRequest) -> JsonResponse:
    with connection.cursor() as cursor:
        cursor.execute(
            '''select r.score as rate, count(t.id) as total from api_track t 
            inner join api_rate r on t.id = r.track_id
            group by r.score
            order by r.score asc'''
        )

        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        data = {"results": []}
        ratings = 0
        for result in results:
            while ratings < result["rate"]:
                data["results"].append({
                    "rate": ratings,
                    "tracks": 0,
                })
                ratings = ratings + 1

            data["results"].append({
                "rate": result["rate"],
                "tracks": result["total"],
            })
            ratings = ratings + 1

        while ratings <= 10:
            data["results"].append({
                "rate": ratings,
                "tracks": 0,
            })
            ratings = ratings + 1

    return JsonResponse(data)


@jwt_auth
@csrf_exempt
@require_http_methods(["GET"])
def audio_features(request: HttpRequest, id: int) -> JsonResponse:
    try:
        track = Track.objects.get(pk=id)

        data = [
            {
                "name": "acousticness",
                "value": "%.2f" % (track.acousticness * 100, )
            },
            {
                "name": "danceability",
                "value": "%.2f" % (track.danceability * 100, )
            },
            {
                "name": "energy",
                "value": "%.2f" % (track.energy * 100, )
            },
            {
                "name": "instrumentalness",
                "value": "%.2f" % (track.instrumentalness * 100, )
            },
            {
                "name": "liveness",
                "value": "%.2f" % (track.liveness * 100, )
            },
            {
                "name": "loudness",
                "value": "%.2f" % (((-60 - track.loudness) * (100 / -60)), )
            },
            {
                "name": "speechiness",
                "value": "%.2f" % (track.speechiness * 100, )
            },
            {
                "name": "valence",
                "value": "%.2f" % (track.valence * 100, )
            },
        ]

        response = JsonResponse({"results": data}, status=200)
    except Track.DoesNotExist:
        response = JsonResponse({'error': 'invalid track'}, status=404)

    return response
