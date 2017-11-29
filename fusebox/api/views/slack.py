import json
import os
import logging
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string
from django.http import HttpResponse, HttpRequest, JsonResponse
from api.formatter import SlackFormatter
from api.helpers.spotify import SpotifyHelper
from api.models import UserProfile
from api.handlers.slack import RATE_CATEGORY_LIKE
from slackclient import SlackClient
from api.helpers.auth import protected


@protected
@csrf_exempt
@require_http_methods(["GET", "POST"])
def subscribe(request: HttpRequest) -> HttpResponse:
    handler = import_string("api.handlers.slack.subscribe")

    return handler(request)


@protected
@csrf_exempt
@require_http_methods(["GET", "POST"])
def unsubscribe(request: HttpRequest) -> HttpResponse:
    handler = import_string("api.handlers.slack.unsubscribe")

    return handler(request)


@protected
@csrf_exempt
@require_http_methods(["GET", "POST"])
def notify(request: HttpRequest) -> HttpResponse:
    track, track_details, played = SpotifyHelper.current_playing_track()
    if track and played:
        user_profiles = UserProfile.objects.filter(
            notifications=True,
            user__is_active=True,
            slack_username__isnull=False
        )
        attachments = SlackFormatter.current_playing_track(
            track,
            category=RATE_CATEGORY_LIKE,
            played=played
        )["attachments"]
        track_url = ": %s" % track.spotify_id if bool(request.GET.get("embed", 0)) else ""
        logging.getLogger(__name__).debug("About to notify %d users." % len(user_profiles))

        sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
        for user_profile in user_profiles:
            logging.getLogger(__name__).debug("Notifying user %s" % user_profile.user.first_name)
            sc.api_call(
                "chat.postMessage",
                channel="%s" % user_profile.slack_username,
                text="Please rate this song to improve our playlist %s" % track_url,
                attachments=attachments,
                username="@%s" % os.getenv("SLACK_USERNAME", "Fusebox"),
                as_user=True
            )
        return HttpResponse("Notified %d users." % len(user_profiles))
    else:
        return HttpResponse("Nothing playing at the moment.")


@protected
@csrf_exempt
@require_http_methods(["POST"])
def proxy(request: HttpRequest) -> JsonResponse:
    valid_commands = [
        "ratesong", "lastsongs", "subscribe", "unsubscribe", "predict", "help", "queue", "dequeue", "playlist"
    ]
    command = request.POST.get("text", "help") if request.POST.get("text", "help") in valid_commands else "help"

    handler = import_string("api.handlers.slack.%s" % command)

    return handler(request)


@protected
@csrf_exempt
@require_http_methods(["POST"])
def interactive(request: HttpRequest) -> HttpResponse:
    data = json.loads(request.POST.get("payload", "{}"))

    logging.getLogger(__name__).debug(request.POST)

    handler = import_string("api.handlers.slack.%s" % data["callback_id"])
    response = handler(data)

    return response
