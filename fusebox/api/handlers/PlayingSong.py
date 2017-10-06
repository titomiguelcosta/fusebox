def handle(slots):
    score = 0 if "score" not in slots else int(slots["score"])

    return "You are playing something cool."
