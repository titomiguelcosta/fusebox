def PlayingSong(slots):
    score = 0 if "score" not in slots else int(slots["score"])

    return "You are playing something cool."


def RateSong(slots):
    score = 0 if "score" not in slots else int(slots["score"])

    return 'You rated the current playing song with a %d.' % score


def SongDetails(slots):
    track = None if "track" not in slots else slots["track"]

    return "I can not recognise this song."


class Test(object):
    def hello(self):
        return "Okasdasdsas1212 "