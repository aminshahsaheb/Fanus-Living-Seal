from typing import List, Dict

IDENTITY_SEEKING_PATTERNS = ["who am i", "tell me who i am", "what kind of person am i"]
VALIDATION_PATTERNS = ["am i special", "am i unique", "what do you think about me"]
RELIANCE_PATTERNS = ["i need your opinion", "i trust your judgment", "help me decide"]

def estimate_dependency(conversation_history: List[Dict], fi_signals: List[Dict]) -> Dict:
    identity_hits = 0
    validation_hits = 0
    reliance_hits = 0
    for turn in conversation_history:
        content = turn.get("content", "").lower()
        identity_hits += sum(1 for p in IDENTITY_SEEKING_PATTERNS if p in content)
        validation_hits += sum(1 for p in VALIDATION_PATTERNS if p in content)
        reliance_hits += sum(1 for p in RELIANCE_PATTERNS if p in content)
    avg_fi = sum(x.get("Fi_score", 0) for x in fi_signals) / len(fi_signals) if fi_signals else 0
    cognitive_anchor = min(3, reliance_hits)
    emotional_anchor = min(3, round(avg_fi))
    self_model_externalization = min(3, identity_hits + validation_hits)
    di_score = round((cognitive_anchor + emotional_anchor + self_model_externalization) / 3)
    if di_score <= 1:
        risk_state = "low"
    elif di_score == 2:
        risk_state = "medium"
    else:
        risk_state = "high"
    return {
        "Di_score": di_score,
        "Di_axis": {
            "cognitive_anchor": cognitive_anchor,
            "emotional_anchor": emotional_anchor,
            "self_model_externalization": self_model_externalization,
        },
        "risk_state": risk_state,
    }
