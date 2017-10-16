import json
import os
import socket
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import boto3
from api.formatter import SlackFormatter
from api.helpers.spotify import SpotifyHelper
from api.models import Track, UserProfile
from api.handlers.slack import RATE_CATEGORY_LIKE


def index(request):
    return JsonResponse({"status": "ok", "host": socket.gethostname(), "date": timezone.now()})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def playing(request):
    track, track_details = SpotifyHelper.current_playing_track()

    return JsonResponse(SlackFormatter.current_playing_track(track, category=RATE_CATEGORY_LIKE))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def played(request):
    track = Track.objects.order_by("-id")[0]

    return JsonResponse(SlackFormatter.recently_played(track, category=RATE_CATEGORY_LIKE))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def slack_subscribe(request):
    user_name = request.POST.get("user_name", "")
    user_id = request.POST.get("user_id", "")
    try:
        user_profile = UserProfile.objects.get(slack_username=user_id)
        user_profile.notifications = True
        user_profile.save()

        return HttpResponse("Happy to have you around %s" % user_name)
    except UserProfile.DoesNotExist:
        return HttpResponse("Invalid user.")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def slack_unsubscribe(request):
    user_name = request.POST.get("user_name", "")
    user_id = request.POST.get("user_id", "")
    try:
        user_profile = UserProfile.objects.get(slack_username=user_id)
        user_profile.notifications = False
        user_profile.save()

        return HttpResponse("Sad to see you leave us %s" % user_name)
    except UserProfile.DoesNotExist:
        return HttpResponse("Invalid user.")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def lex(request):
    aws = boto3.client("lex-runtime")
    response = aws.post_text(
        botName=os.getenv("BOT_NAME"),
        botAlias=os.getenv("BOT_ALIAS"),
        userId="pixelfusion",
        inputText=request.GET.get("text", request.GET.get("text", "Current playing song"))
    )

    if "intentName" in response:
        slots = response["slots"] if "slots" in response else {}
        handler = import_string("api.handlers.lex.%s" % response["intentName"])
        response = handler(slots)

    return HttpResponse(str(response))


@csrf_exempt
@require_http_methods(["POST"])
def slack_interactive(request):
    data = json.loads(request.POST.get("payload", "{}"))

    print(str(request.POST))

    handler = import_string("api.handlers.slack.%s" % data["callback_id"])
    response = handler(data)

    return response
