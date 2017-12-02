from django.core.management.base import BaseCommand
from api.services import get_spotify
from api.models import Track, Playlist, PlaylistTracks, UserProfile
import boto3
import os
import logging
from slackclient import SlackClient
import signal
import json
import requests
from django.utils import timezone


class Command(BaseCommand):
    help = "Pulls messages from SQS and (de)queues songs from the Fusebox playlist"

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout=stdout, stderr=stderr, no_color=no_color)
        self.kill_now = False

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def add_arguments(self, parser):
        pass

    def exit_gracefully(self, signum, frame):
        logging.getLogger(__name__).warning("About to terminate")
        self.kill_now = True

    def handle(self, *args, **options):
        sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
        sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'ap-southeast-2'))

        while True:
            if self.kill_now:
                break

            # in the loop so we can refresh the token if needed
            spotify_client = get_spotify()

            response = sqs.receive_message(
                QueueUrl=os.getenv('SLACK_PLAYLIST_QUEUE'),
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20,
                VisibilityTimeout=60,
                MessageAttributeNames=['All']
            )

            if 'Messages' not in response:
                continue

            for sqs_msg in response['Messages']:
                try:
                    body = json.loads(sqs_msg['Body'])
                except json.decoder.JSONDecodeError as e:
                    logging.getLogger(__name__).error("Invalid json: " + str(e))
                    continue

                action = body["action"]
                title = body["search"]["q"]
                user_slack_id = body["user"]["slack_id"]

                tracks = spotify_client.search(title, limit=1)
                if 1 == len(tracks["tracks"]["items"]):
                    try:
                        track_details = tracks["tracks"]["items"][0]

                        self.update_models(
                            track_details, action, user_slack_id, spotify_client._get_uri('track', track_details['id'])
                        )

                        if "queue" == action:
                            spotify_client.user_playlist_add_tracks(
                                os.getenv("SPOTIPY_USERNAME"),
                                os.getenv("SPOTIFY_PLAYLIST_ID"),
                                [track_details["id"]]
                            )
                        elif "dequeue" == action:
                            spotify_client.user_playlist_remove_all_occurrences_of_tracks(
                                os.getenv("SPOTIPY_USERNAME"),
                                os.getenv("SPOTIFY_PLAYLIST_ID"),
                                [track_details["id"]]
                            )

                        sc.api_call(
                            "chat.postMessage",
                            channel=user_slack_id,
                            text="The song *%s* by *%s* was %sd from the Fusebox playlist" % (
                                track_details["name"],
                                track_details["artists"][0]["name"],
                                action
                            ),
                            markdown=True,
                            username="@%s" % os.getenv("SLACK_USERNAME", "Fusebox"),
                            as_user=True
                        )

                        requests.post(os.getenv("SPOTIPY_CHANNEL_URL"), json={
                            "text": "@%s just %sd *%s* by *%s*" % (
                                body["user"]["name"], action, track_details["name"], track_details["artists"][0]["name"]
                            )
                        })
                    except Exception as e:
                        logging.getLogger(__name__).error("Something failed: " + str(e))
                else:
                    sc.api_call(
                        "chat.postMessage",
                        channel=user_slack_id,
                        text="No results for the song *%s*" % title,
                        markdown=True,
                        username="@%s" % os.getenv("SLACK_USERNAME", "Fusebox"),
                        as_user=True
                    )

                sqs.delete_message(
                    QueueUrl=os.getenv('SLACK_PLAYLIST_QUEUE'),
                    ReceiptHandle=sqs_msg['ReceiptHandle']
                )

    def update_models(self, track_details, action, user_slack_id, track_uri):
        try:
            user_profile = UserProfile.objects.get(slack_username=user_slack_id)
        except UserProfile.DoesNotExist:
            return None

        try:
            track = Track.objects.get(spotify_id=track_uri)
        except Track.DoesNotExist:
            track = Track()
            track.title = track_details['name']
            track.spotify_id = track_uri
            track.album = track_details['album']['name']
            track.save()

        try:
            playlist = Playlist.objects.get(name="Fusebox")
        except Playlist.DoesNotExist:
            playlist = Playlist()
            playlist.name = "Fusebox"
            playlist.spotify_id = os.getenv("SPOTIFY_PLAYLIST_ID")
            playlist.save()

        try:
            playlist_tracks = PlaylistTracks.objects.get(
                track=track, playlist=playlist
            )
        except PlaylistTracks.DoesNotExist:
            playlist_tracks = PlaylistTracks()
            playlist_tracks.track = track
            playlist_tracks.playlist = playlist

        if "queue" == action:
            playlist_tracks.queued_by = user_profile.user
            playlist_tracks.queued_on = timezone.now()
        elif "dequeue" == action:
            playlist_tracks.dequeued_by = user_profile.user
            playlist_tracks.dequeued_on = timezone.now()

        playlist_tracks.save()
