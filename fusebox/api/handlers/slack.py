from django.http import HttpResponse, JsonResponse, HttpRequest
from django.utils import timezone
import requests
import os
import random
from api.models import Track, UserProfile, Rate, Played
from api.formatter import SlackFormatter
from api.helpers.spotify import SpotifyHelper


MESSAGE_RATE_LIMIT = 3
RATE_CATEGORY_LIKE = 1


def ratesong(request: HttpRequest) -> JsonResponse:
    track, track_details, played = SpotifyHelper.current_playing_track()

    return JsonResponse(SlackFormatter.current_playing_track(track, category=RATE_CATEGORY_LIKE, played=played))


def lastsongs(request: HttpRequest) -> JsonResponse:
    try:
        played = Played.objects.order_by("-id")[0]
        response = SlackFormatter.recently_played(played.track, category=RATE_CATEGORY_LIKE, played=played)
    except IndexError:
        response = {"text": "No song has ever been played."}

    return JsonResponse(response)


def help(request: HttpRequest):
    return JsonResponse({"text": "Available commands: ratesong, lastsongs, subscribe, unsubscribe and help"})


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


def rate_track(data):
    # value is a string in format score:played_id:counter:category
    score, played_id, counter, category_id = list(map(int, data["actions"][0]["value"].split(":")))
    thanks = [
        "Thanks for rating this song, enjoy the rest of your day!",
        "Got it. Who's awesome? You're awesome!",
        "You just helped make this office a better place.",
        "All done. Feel free keep rating songs throughout the day.",
        "That's exactly what I would've rated it, too!",
        "Your rating is music to my ears.",
        "Remember: The more you vote the smarter I get.",
        "As a wise person once said: \"Please don't stop the music.\"",
        "Sweet as.",
        "Look at you sharing your musical feels. Way to go!",
        "Thank you, I appreciate it.",
        "Cheers for that, this will make my research so much easier.",
        "Alright, I made a note of that."
    ]
    response = HttpResponse(random.choice(thanks))
    if counter <= MESSAGE_RATE_LIMIT:
        try:
            played = Played.objects.get(pk=played_id)
            track = played.track
            user_profile = UserProfile.objects.get(slack_username=data["user"]["id"])

            if user_profile and track:
                requests.post(os.getenv("SPOTIPY_CHANNEL_URL"), json={
                    "text": "@%s just rated *%s* by *%s*" % (data["user"]["name"], track.title, track.artists_to_str)
                })

                rate = Rate()
                rate.user = user_profile.user
                rate.track = track
                rate.category = get_rate_category(category_id)
                rate.score = score
                rate.on = timezone.now()
                rate.save()

                if counter < MESSAGE_RATE_LIMIT:
                    try:
                        previous_played = Played.objects.order_by("-id").filter(pk__lt=played_id)[0]
                        previous_track = previous_played.track
                        response = JsonResponse(
                            SlackFormatter.recently_played(
                                previous_track, category=RATE_CATEGORY_LIKE, played=previous_played, counter=1+counter
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
