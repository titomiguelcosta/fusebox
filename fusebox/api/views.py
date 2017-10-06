import json
import os
import socket
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string
from django.http import HttpResponse, JsonResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
import boto3
import requests

def index(request):
    return JsonResponse({"status": "ok", "host": socket.gethostname()})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def playing(request):
    oauth = SpotifyOAuth(
        os.getenv("SPOTIPY_CLIENT_ID"),
        os.getenv("SPOTIPY_CLIENT_SECRET"),
        os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-library-read user-read-currently-playing",
        cache_path=settings.BASE_DIR+"/../.cache-" + os.getenv("SPOTIPY_USERNAME")
    )
    sp = spotipy.Spotify(auth=str(oauth.get_cached_token()["access_token"]))
    track = sp._get("me/player/currently-playing")

    requests.post("https://hooks.slack.com/services/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", json={"text": str(track)})

    return HttpResponse(str(track))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def lex(request):
    aws = boto3.client("lex-runtime")
    response = aws.post_text(
        botName=os.getenv("BOT_NAME"),
        botAlias=os.getenv("BOT_ALIAS"),
        userId="pixelfusion",
        inputText='Current playing song'
    )

    if "intentName" in response:
        slots = response["slots"] if "slots" in response else {}
        handler = import_string("api.handlers.%s.handle" % response["intentName"])
        response = handler(slots)

    return HttpResponse(str(response))


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
    print(data)

    # if "event" in data and "bot_id" not in data["event"] and "channel" in data["event"]:
    #     sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
    #     sc.api_call(
    #         "chat.postMessage",
    #         channel=data["event"]["channel"],
    #         text="Hello from Python! :tada:"
    #     )

    return HttpResponse('adsasdasdas')
