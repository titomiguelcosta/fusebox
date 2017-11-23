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

    writer = csv.writer(response, fieldnames=fieldnames)
    writer.writeheader()

    for track in tracks:
        writer.writerow({
            "artist": track.artists_to_str,
            "album": track.album,
            "title": track.title,
            "danceability": track.danceability,
            "energy": track.energy,
            "loudness": track.loudness,
            "speechiness": track.speechiness,
            "acousticness": track.acousticness,
            "instrumentalness": track.instrumentalness,
            "liveness": track.liveness,
            "valence": track.valence,
            "tempo": track.tempo,
            "duration_ms": track.duration_ms,
            "num_played": 0,
            "rate": 0.0
        })

    return response
