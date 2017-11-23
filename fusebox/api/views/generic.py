import socket
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string
from api.helpers.auth import protected
from api.models import Track
import csv


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok", "host": socket.gethostname(), "date": timezone.now()})


@protected
@csrf_exempt
@require_http_methods(["POST"])
def proxy(request: HttpRequest) -> JsonResponse:
    valid_commands = ["ratesong", "lastsongs", "subscribe", "unsubscribe", "help"]
    command = request.POST.get("text", "help") if request.POST.get("text", "help") in valid_commands else "help"

    handler = import_string("api.handlers.slack.%s" % command)

    return handler(request)


@protected
def dump(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fusebox.csv"'

    fieldnames = [
        "artist", "album", "title", "danceability", "energy", "loudness",
        "speechiness", "acousticness", "instrumentalness", "liveness",
        "valence", "tempo", "duration_ms", "num_played", "rate"
    ]
    tracks = Track.objects.raw(
        '''select t.id, avg(r.score) as rate, count(distinct p.id) as num_played from api_track t 
            inner join api_played p on t.id = p.track_id
            inner join api_rate r on r.track_id = t.id
            group by t.id'''
    )

    writer = csv.writer(response)
    writer.writerow(fieldnames)

    for track in tracks:
        writer.writerow([
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
