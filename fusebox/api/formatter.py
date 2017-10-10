class SlackFormatter(object):
    @staticmethod
    def current_playing_track(track):
        return {
            "text": "Currently playing",
            "attachments": [
                {
                    "title": track.title,
                    "title_link": track.url,
                    "fields": [
                        {
                            "title": "Album",
                            "value": track.album,
                            "short": True
                        },
                        {
                            "title": "Artist",
                            "value": track.artists_to_str,
                            "short": True
                        },
                    ],
                    "image_url": track.spotify_id
                },
                {
                    "title": "How do you rate it?",
                    "fallback": "You were unable to rate.",
                    "callback_id": "rate_currently_playing_track",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "rate",
                            "text": "Hate",
                            "type": "button",
                            "value": "1"
                        },
                        {
                            "name": "rate",
                            "text": "It's OK",
                            "type": "button",
                            "value": "3"
                        },
                        {
                            "name": "rate",
                            "text": "Not sure",
                            "type": "button",
                            "value": "5"
                        },
                        {
                            "name": "rate",
                            "text": "Like",
                            "style": "danger",
                            "type": "button",
                            "value": "7",
                        },
                        {
                            "name": "rate",
                            "text": "Love it",
                            "style": "danger",
                            "type": "button",
                            "value": "9",
                        }
                    ]
                }
            ]
        }

    @staticmethod
    def recently_played(tracks):
        data = {
            "text": "Recently played",
            "attachments": []
        }

        for track in tracks:
            data["attachments"].append(
                {
                    "title": track.title,
                    "title_link": track.url,
                    "fields": [
                        {
                            "title": "Album",
                            "value": track.album,
                            "short": True
                        },
                        {
                            "title": "Artist",
                            "value": track.artists_to_str,
                            "short": True
                        },
                    ]
                }
            )
            data["attachments"].append(
                {
                    "title": "How do you rate it?",
                    "fallback": "You were unable to rate.",
                    "callback_id": "rate_currently_playing_track",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "rate",
                            "text": "Hate",
                            "type": "button",
                            "value": "1"
                        },
                        {
                            "name": "rate",
                            "text": "It's OK",
                            "type": "button",
                            "value": "3"
                        },
                        {
                            "name": "rate",
                            "text": "Not sure",
                            "type": "button",
                            "value": "5"
                        },
                        {
                            "name": "rate",
                            "text": "Like",
                            "style": "danger",
                            "type": "button",
                            "value": "7",
                        },
                        {
                            "name": "rate",
                            "text": "Love it",
                            "style": "danger",
                            "type": "button",
                            "value": "9",
                        }
                    ]
                }
            )

        return data
