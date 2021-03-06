from django.core.management.base import BaseCommand
from api.services import get_spotify
import boto3
import os
import logging
from slack import WebClient
from api.models import Played
import signal
import json
import requests


class Command(BaseCommand):
    help = "Pulls messages from a queue a notifies users about the prediction they requested"

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
        sc = WebClient(os.getenv("SLACK_API_TOKEN"))
        sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'ap-southeast-2'))

        while True:
            if self.kill_now:
                break

            response = sqs.receive_message(
                QueueUrl=os.getenv('SLACK_PREDICT_QUEUE'),
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20,
                VisibilityTimeout=60,
                MessageAttributeNames=['All']
            )

            if 'Messages' not in response:
                continue

            # in the loop so we can refresh the token if needed
            spotify_client = get_spotify()

            for sqs_msg in response['Messages']:
                try:
                    body = json.loads(sqs_msg['Body'])
                except json.decoder.JSONDecodeError as e:
                    logging.getLogger(__name__).error("Invalid json: " + str(e))
                    continue

                title = body["search"]["q"]
                slack_id = body["user"]["slack_id"]

                tracks = spotify_client.search(title, limit=1)
                if 1 == len(tracks["tracks"]["items"]):
                    try:
                        track = tracks["tracks"]["items"][0]
                        track_details = spotify_client._get("audio-features/" + track["id"])

                        aws_client = boto3.client('machinelearning', region_name="us-east-1")
                        predicted = aws_client.predict(
                            MLModelId=os.getenv('ML_MODEL_ID', 'ml-0vlfzxpmeGb'),
                            Record={
                                'id': track["id"],
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
                            channel=slack_id,
                            text="The song *%s* by *%s* got a predicted rate of %.2f" % (
                                track["name"],
                                track["artists"][0]["name"],
                                predicted["Prediction"]["predictedValue"]
                            ),
                            markdown=True,
                            username="@%s" % os.getenv("SLACK_USERNAME", "Fusebox"),
                            as_user=True
                        )

                        requests.post(os.getenv("SPOTIPY_SLACK_CHANNEL_URL"), json={
                            "text": "@%s checked prediction for *%s* by *%s*" % (
                                body["user"]["name"], track["name"], track["artists"][0]["name"]
                            )
                        })
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
                    QueueUrl=os.getenv('SLACK_PREDICT_QUEUE'),
                    ReceiptHandle=sqs_msg['ReceiptHandle']
                )
