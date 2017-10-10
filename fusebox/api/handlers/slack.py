def rate_currently_playing_track(data):
    # requests.post(os.getenv("SPOTIPY_CHANNEL_URL"), json={"text": "Thanks for voting."})

    # if "event" in data and "bot_id" not in data["event"] and "channel" in data["event"]:
    #     sc = SlackClient(os.getenv("SLACK_API_TOKEN"))
    #     sc.api_call(
    #         "chat.postMessage",
    #         channel=data["event"]["channel"],
    #         text="Hello from Python! :tada:"
    #     )

    return "Thanks for voting."
