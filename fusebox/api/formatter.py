class SlackFormatter(object):
    @staticmethod
    def current_playing_track(track, category):
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
                            "short": True,
                            "color": "#3AA3E3",
                        },
                        {
                            "title": "Artist",
                            "value": track.artists_to_str,
                            "short": True,
                            "color": "#FF0000",
                        },
                    ],
                    "image_url": track.spotify_id
                },
                {
                    "title": "How do you feel about this song?",
                    "fallback": "You were unable to rate.",
                    "callback_id": "rate_track",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "rate",
                            "text": ":scream:",
                            "type": "button",
                            "value": "1:%s:3:%s" % (track.id, category)
                        },
                        {
                            "name": "rate",
                            "text": ":thumbsdown:",
                            "type": "button",
                            "value": "3:%s:3:%s" % (track.id, category)
                        },
                        {
                            "name": "rate",
                            "text": ":neutral_face:",
                            "type": "button",
                            "value": "5:%s:3:%s" % (track.id, category)
                        },
                        {
                            "name": "rate",
                            "text": ":thumbsup:",
                            "type": "button",
                            "value": "7:%s:3:%s" % (track.id, category)
                        },
                        {
                            "name": "rate",
                            "text": ":heart_eyes:",
                            "type": "button",
                            "value": "9:%s:3:%s" % (track.id, category)
                        }
                    ]
                }
            ]
        }

    @staticmethod
    def recently_played(track, category, counter=1):
        data = {
            "text": "Recently played",
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
                    ]
                },
                {
                    "title": "How do you feel about this song?",
                    "fallback": "You were unable to rate.",
                    "callback_id": "rate_track",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "rate",
                            "text": ":scream:",
                            "type": "button",
                            "value": "1:%s:%s:%s" % (track.id, counter, category)
                        },
                        {
                            "name": "rate",
                            "text": ":thumbsdown:",
                            "type": "button",
                            "value": "3:%s:%s:%s" % (track.id, counter, category)
                        },
                        {
                            "name": "rate",
                            "text": ":neutral_face:",
                            "type": "button",
                            "value": "5:%s:%s:%s" % (track.id, counter, category)
                        },
                        {
                            "name": "rate",
                            "text": ":thumbsup:",
                            "type": "button",
                            "value": "7:%s:%s:%s" % (track.id, counter, category)
                        },
                        {
                            "name": "rate",
                            "text": ":heart_eyes:",
                            "type": "button",
                            "value": "9:%s:%s:%s" % (track.id, counter, category)
                        }
                    ]
                }
            ]
        }

        return data
