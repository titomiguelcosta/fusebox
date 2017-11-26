from django.http import HttpResponse, JsonResponse, HttpRequest
from django.utils import timezone
import requests
import os
import random
from slackclient import SlackClient
from api.models import Track, UserProfile, Rate, Played
from api.formatter import SlackFormatter
from api.helpers.spotify import SpotifyHelper
from api.services import get_spotify
import logging
import boto3

MESSAGE_RATE_LIMIT = 3
RATE_CATEGORY_LIKE = 1

# Endpoints for the command /fusebox [operation]


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


def predict(request: HttpRequest) -> HttpResponse:
    sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
    sc.api_call(
        "dialog.open",
        channel=request.POST.get("channel_id"),
        token=request.POST.get("token"),
        trigger_id=request.POST.get("trigger_id"),
        dialog={
            "callback_id": "prediction",
            "title": "Fusebox Dev",
            "submit_label": "Prediction",
            "elements": [
                {
                    "type": "text",
                    "label": "Title of the song",
                    "name": "title",
                }
            ]
        },
        username="@%s" % os.getenv("SLACK_USERNAME", "Fusebox"),
        as_user=True
    )

    return HttpResponse("")


def help(request: HttpRequest):
    return JsonResponse({"text": "Available commands: ratesong, lastsongs, subscribe, unsubscribe and predict"})


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


# Interaction commands

def prediction(data) -> HttpResponse:
    title = data["submission"]["title"]
    if len(title) > 0:
        sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
        spotify_client = get_spotify()
        tracks = spotify_client.search(title, limit=1)
        logging.getLogger(__name__).debug(tracks)
        if 1 == len(tracks["tracks"]["items"]):
            try:
                track = tracks["tracks"]["items"][0]
                track_details = spotify_client._get("audio-features/" + track["id"])

                aws_client = boto3.client('machinelearning', region_name="us-east-1")
                predicted = aws_client.predict(
                    MLModelId='ml-M8WNNOAV6oy',
                    Record={
                        'title': track["name"],
                        'album': track["album"]["name"],
                        'artist': track["artists"][0]["name"],
                        'danceability': str(track_details["danceability"]),
                        'energy': str(track_details["energy"]),
                        'loudness': str(track_details["loudness"]),
                        'speechiness': str(track_details["speechiness"]),
                        'acousticness': str(track_details["acousticness"]),
                        'instrumentalness': str(track_details["instrumentalness"]),
                        'liveness': str(track_details["liveness"]),
                        'valence': str(track_details["valence"]),
                        'tempo': str(track_details["tempo"]),
                        'duration_ms': str(track_details["duration_ms"]),
                        'played': str(Played.objects.filter(track__spotify_id=track["id"]).count())
                    },
                    PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'
                )
                sc.api_call(
                    "chat.postMessage",
                    channel=data["user"]["id"],
                    text="The song *%s* by *%s* got a predicted rate of %.2f" % (
                        track["name"],
                        track["artists"][0]["name"],
                        predicted["Prediction"]["predictedValue"]
                    ),
                    markdown=True,
                    username="@%s" % os.getenv("SLACK_USERNAME", "Fusebox"),
                    as_user=True
                )
            except Exception as e:
                logging.getLogger(__name__).error("Something failed: " + str(e))

        response = HttpResponse("")
    else:
        logging.getLogger(__name__).error("Invalid song title: %s" % title)
        response = JsonResponse({
            "errors": [
                {
                    "name": "title",
                    "error": "Invalid title"
                }
            ]
        })

    return response


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
                rate.category = _get_rate_category(category_id)
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


def _get_rate_category(category_id):
    categories = {RATE_CATEGORY_LIKE: "like"}

    return categories[category_id] if category_id in categories else "like"
