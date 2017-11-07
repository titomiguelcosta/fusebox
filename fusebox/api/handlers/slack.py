from django.http import HttpResponse, JsonResponse
from api.models import Track, UserProfile, Rate
from api.formatter import SlackFormatter
from django.utils import timezone
import requests
import os
import random

MESSAGE_RATE_LIMIT = 3
RATE_CATEGORY_LIKE = 1


def rate_track(data):
    # value is a string in format score:track_id:counter:category
    score, track_id, counter, category_id = list(map(int, data["actions"][0]["value"].split(":")))
    thanks = ["Thanks for voting.", "Fantastic. Much appreciated.", "Glorious. Your vote counts."]
    response = HttpResponse(random.choice(thanks))
    if counter <= MESSAGE_RATE_LIMIT:
        try:
            track = Track.objects.get(pk=track_id)
            user_profile = UserProfile.objects.get(slack_username=data["user"]["id"])

            if user_profile and track:
                requests.post(os.getenv("SPOTIPY_CHANNEL_URL"), json={"text": "@%s just rated *%s* by *%s*" % (data["user"]["name"], track.title, track.artists_to_str)})

                rate = Rate()
                rate.user = user_profile.user
                rate.track = track
                rate.category = get_rate_category(category_id)
                rate.score = score
                rate.on = timezone.now()
                rate.save()

                if counter < MESSAGE_RATE_LIMIT:
                    try:
                        previous_track = Track.objects.order_by("-id").filter(pk__lt=track_id)[0]
                        response = JsonResponse(
                            SlackFormatter.recently_played(
                                previous_track, category=RATE_CATEGORY_LIKE, counter=1+counter
                            )
                        )
                    except Track.DoesNotExist:
                        response = HttpResponse("Failed to retrieve previous song.")
            else:
                response = HttpResponse("System is not aware of your user.")
        except Track.DoesNotExist:
            response = HttpResponse("Sorry. Song is not available.")

    return response


def get_rate_category(category_id):
    categories = {RATE_CATEGORY_LIKE: "like"}

    return categories[category_id] if category_id in categories else "like"
