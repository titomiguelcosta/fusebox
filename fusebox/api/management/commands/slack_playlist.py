from django.core.management.base import BaseCommand
from api.services import get_spotify
import boto3
import os
import logging
from slackclient import SlackClient
import signal
import json


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
        spotify_client = get_spotify()
        sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'ap-southeast-2'))

        while True:
            if self.kill_now:
                break

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
                slack_id = body["user"]["slack_id"]

                tracks = spotify_client.search(title, limit=1)
                if 1 == len(tracks["tracks"]["items"]):
                    try:
                        track = tracks["tracks"]["items"][0]
                        if "queue" == action:
                            spotify_client.user_playlist_add_tracks(
                                os.getenv("SPOTIPY_USERNAME"),
                                os.getenv("SPOTIFY_PLAYLIST_ID"),
                                [track["id"]]
                            )
                        elif "dequeue" == action:
                            spotify_client.user_playlist_remove_all_occurrences_of_tracks(
                                os.getenv("SPOTIPY_USERNAME"),
                                os.getenv("SPOTIFY_PLAYLIST_ID"),
                                [track["id"]]
                            )

                        sc.api_call(
                            "chat.postMessage",
                            channel=slack_id,
                            text="The song *%s* by *%s* was %sd from the Fusebox playlist" % (
                                track["name"],
                                track["artists"][0]["name"],
                                action
                            ),
                            markdown=True,
                            username="@%s" % os.getenv("SLACK_USERNAME", "Fusebox"),
                            as_user=True
                        )
                    except Exception as e:
                        logging.getLogger(__name__).error("Something failed: " + str(e))
                else:
                    sc.api_call(
                        "chat.postMessage",
                        channel=slack_id,
                        text="No results for the song *%s*" % title,
                        markdown=True,
                        username="@%s" % os.getenv("SLACK_USERNAME", "Fusebox"),
                        as_user=True
                    )

                sqs.delete_message(
                    QueueUrl=os.getenv('SLACK_PLAYLIST_QUEUE'),
                    ReceiptHandle=sqs_msg['ReceiptHandle']
                )
