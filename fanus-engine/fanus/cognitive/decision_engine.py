def decide(intent: str):
    if intent == "bug_fix":
        return "ALLOW"

    if intent == "unknown":
        return "REVIEW"

    return "ALLOW"
