from django.core.management.base import BaseCommand
from api.helpers.spotify import SpotifyHelper
from api.models import UserProfile
from slackclient import SlackClient
from api.formatter import SlackFormatter
from api.handlers.slack import RATE_CATEGORY_LIKE
import os


class Command(BaseCommand):
    help = "Notify slack users about the current playing track"

    def handle(self, *args, **options):
        track, track_details, played = SpotifyHelper.current_playing_track()
        if track and played:
            user_profiles = UserProfile.objects.filter(
                notifications=True, user__is_active=True, slack_username__isnull=False
            )
            print("About to notify %d users." % len(user_profiles))
            for user_profile in user_profiles:
                print("Notifying user %s" % user_profile.user.first_name)
                sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
                sc.api_call(
                    "chat.postMessage",
                    channel="%s" % user_profile.slack_username,
                    text="Please rate this song to improve our playlist",
                    attachments=SlackFormatter.current_playing_track(
                        track, category=RATE_CATEGORY_LIKE, played=played
                    )["attachments"],
                    username="@%s" % os.getenv("SLACK_USERNAME", "Fusebox"),
                    as_user=True
                )
        else:
            print("Nothing playing at the moment.")
