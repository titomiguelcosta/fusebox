from api.models import Track
from api.helpers.auth import jwt_auth, get_user_from_jwt_token
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest


@jwt_auth
@csrf_exempt
@require_http_methods(["GET"])
def tracks_per_artist(request: HttpRequest) -> JsonResponse:
    tracks = Track.objects.raw(
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
