def analyze_intent(diff_text: str):
    """
    Detect why change happened
    """
    if "fix" in diff_text:
        return "bug_fix"

    if "refactor" in diff_text:
        return "refactor"

    if "memory" in diff_text:
        return "memory_update"

    return "unknown"
