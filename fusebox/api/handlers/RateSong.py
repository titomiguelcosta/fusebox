def handle(slots):
    score = 0 if "score" not in slots else int(slots["score"])

    return 'You rated the current playing song with a %d.' % score
