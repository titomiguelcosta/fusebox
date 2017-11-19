import json
import os
import socket
import logging
import boto3
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from api.formatter import SlackFormatter
from api.helpers.spotify import SpotifyHelper
from api.models import UserProfile, Played, User, Track
from api.handlers.slack import RATE_CATEGORY_LIKE
from slackclient import SlackClient
from api.services import get_spotify


def index(request):
    return JsonResponse({"status": "ok", "host": socket.gethostname(), "date": timezone.now()})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def playing(request):
    track, track_details, played = SpotifyHelper.current_playing_track()

    return JsonResponse(SlackFormatter.current_playing_track(track, category=RATE_CATEGORY_LIKE, played=played))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def played(request):
    try:
        played = Played.objects.order_by("-id")[0]
        response = SlackFormatter.recently_played(played.track, category=RATE_CATEGORY_LIKE, played=played)
    except IndexError:
        response = {"text": "No songs have ever been played."}

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def tracks_populate(request):
    client = get_spotify()
    tracks = Track.objects.filter(populate=False, spotify_id__isnull=False)
    errors = []
    for track in tracks:
        try:
            data = client._get("audio-features/"+track.spotify_id)
        except Exception as e:
            errors.append(str(e))
            continue

        track.danceability = data["danceability"]
        track.energy = data["energy"]
        track.loudness = data["loudness"]
        track.speechiness = data["speechiness"]
        track.acousticness = data["acousticness"]
        track.instrumentalness = data["instrumentalness"]
        track.liveness = data["liveness"]
        track.valence = data["valence"]
        track.tempo = data["tempo"]
        track.duration_ms = data["duration_ms"]
        track.populated = True
        track.save()

    return JsonResponse({"populated": len(tracks), "errors": errors})


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
def slack_notify(request):
    track, track_details, played = SpotifyHelper.current_playing_track()
    if track and played:
        user_profiles = UserProfile.objects.filter(notifications=True, user__is_active=True,
                                                   slack_username__isnull=False)
        logging.getLogger(__name__).debug("About to notify %d users." % len(user_profiles))
        for user_profile in user_profiles:
            logging.getLogger(__name__).debug("Notifying user %s" % user_profile.user.first_name)
            sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
            sc.api_call(
                "chat.postMessage",
                channel="%s" % user_profile.slack_username,
                text="Please rate this song to improve our playlist",
                attachments=SlackFormatter.current_playing_track(track, category=RATE_CATEGORY_LIKE, played=played)["attachments"],
                username="@Fusebox",
                as_user=True

            )
        return HttpResponse("Notified %d users." % len(user_profiles))
    else:
        return HttpResponse("Nothing playing at the moment.")


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

    logging.getLogger(__name__).debug(request.POST)

    handler = import_string("api.handlers.slack.%s" % data["callback_id"])
    response = handler(data)

    return response


def users_populate(request):
    sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
    response = sc.api_call("users.list")
    data = []

    for slack_user in response["members"]:
        if "profile" in slack_user \
                and "email" in slack_user["profile"] \
                and slack_user["profile"]["email"].endswith("pixelfusion.co.nz"):
            try:
                user_profile = UserProfile.objects.get(slack_username=slack_user["id"])
                user = user_profile.user
            except UserProfile.DoesNotExist:
                user_profile = UserProfile()
                user = User()

            user.username = slack_user["id"]
            user.email = slack_user["profile"]["email"]
            user.first_name = slack_user["profile"]["real_name"]
            user.set_password("Q12w3esw1ddn")
            user.is_active = not slack_user["deleted"]
            user.is_superuser = slack_user["is_admin"] if "is_admin" in slack_user else False
            user.save()

            user_profile.slack_username = slack_user["id"]
            user_profile.user = user
            user_profile.save()

            data.append("User %s synced." % slack_user["profile"]["real_name"])

    return JsonResponse(data, safe=False)
