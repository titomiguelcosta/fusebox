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
    tracks = Track.objects.filter(populated=True)

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
            0,
            0.0
        ])

    return response
