import json
import os
import logging
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string
from django.http import HttpResponse, HttpRequest
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
    user_name = request.POST.get("user_name", "")
    user_id = request.POST.get("user_id", "")
    try:
        user_profile = UserProfile.objects.get(slack_username=user_id)
        user_profile.notifications = True
        user_profile.save()

        return HttpResponse("Happy to have you around %s" % user_name)
    except UserProfile.DoesNotExist:
        return HttpResponse("Invalid user.")


@protected
@csrf_exempt
@require_http_methods(["GET", "POST"])
def unsubscribe(request: HttpRequest) -> HttpResponse:
    user_name = request.POST.get("user_name", "")
    user_id = request.POST.get("user_id", "")
    try:
        user_profile = UserProfile.objects.get(slack_username=user_id)
        user_profile.notifications = False
        user_profile.save()

        return HttpResponse("Sad to see you leave us %s" % user_name)
    except UserProfile.DoesNotExist:
        return HttpResponse("Invalid user.")


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
        for user_profile in user_profiles:
            logging.getLogger(__name__).debug("Notifying user %s" % user_profile.user.first_name)
            sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
            sc.api_call(
                "chat.postMessage",
                channel="%s" % user_profile.slack_username,
                text="Please rate this song to improve our playlist %s" % track_url,
                attachments=attachments,
                username="@Fusebox",
                as_user=True
            )
        return HttpResponse("Notified %d users." % len(user_profiles))
    else:
        return HttpResponse("Nothing playing at the moment.")


@protected
@csrf_exempt
@require_http_methods(["POST"])
def interactive(request: HttpRequest) -> HttpResponse:
    data = json.loads(request.POST.get("payload", "{}"))

    logging.getLogger(__name__).debug(request.POST)

    handler = import_string("api.handlers.slack.%s" % data["callback_id"])
    response = handler(data)

    return response
