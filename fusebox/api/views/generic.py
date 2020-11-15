import socket
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.utils import timezone
from api.helpers.auth import query_auth
from api.models import Track
import csv


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok", "host": socket.gethostname(), "date": timezone.now()})


@query_auth
def dump(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fusebox.csv"'

    fieldnames = [
        "id", "artist", "album", "title", "key", "time_signature", "danceability", "energy", "loudness",
        "speechiness", "acousticness", "instrumentalness", "liveness",
        "valence", "tempo", "duration_ms", "num_played", "num_rates", "rate"
    ]
    tracks = Track.objects.raw(
        '''select
                t.*, avg(r.score) as rate, count(distinct p.id) as num_played, count(distinct r.id) as num_rates
            from api_track t
            inner join api_played p on t.id = p.track_id
            inner join api_rate r on r.track_id = t.id
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
            track.key,
            track.time_signature,
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
            track.num_rates,
            track.rate
        ])

    return response
