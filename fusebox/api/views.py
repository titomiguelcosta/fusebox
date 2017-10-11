import json
import os
import socket
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import boto3
import requests
from api.formatter import SlackFormatter
from api.helpers.spotify import SpotifyHelper
from api.models import Track


def index(request):
    return JsonResponse({"status": "ok", "host": socket.gethostname(), "date": timezone.now()})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def playing(request):
    track, track_details = SpotifyHelper.current_playing_track()
    requests.post(os.getenv("SPOTIPY_CHANNEL_URL"), json={"text": "@%s requested current playing song. Listening to %s" % (request.POST.get("user_name", "Someone"), track.title)})

    return JsonResponse(SlackFormatter.current_playing_track(track))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def played(request):
    requests.post(os.getenv("SPOTIPY_CHANNEL_URL"), json={"text": "@%s requested recently played song." % request.POST.get("user_name", "Someone")})

    tracks = Track.objects.all().order_by("-id")[:3]

    return JsonResponse(SlackFormatter.recently_played(tracks))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def rate(request, score):
    track, track_details = SpotifyHelper.current_playing_track()
    if track:
        requests.post(os.getenv("SPOTIPY_CHANNEL_URL"), json={"text": "%s just rated track %s" % ("me", track.title)})

    return HttpResponse("Thanks for rating.")


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
    data = json.loads(request.POST.get("payload"))

    handler = import_string("api.handlers.slack.%s" % data["callback_id"])
    response = handler(data)

    return HttpResponse(response)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def slack_listener(request):
    data = json.loads(request.body)
    # FLOW #####
    # Get body message
    # Pass to Lex
    # Grab intent
    # Execute action
    # Post reply to slack

    # if "event" in data and "bot_id" not in data["event"] and "channel" in data["event"]:
    #     sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
    #     sc.api_call(
    #         "chat.postMessage",
    #         channel=data["event"]["channel"],
    #         text="Hello from Python! :tada:"
    #     )

    return HttpResponse('To be implemented')
