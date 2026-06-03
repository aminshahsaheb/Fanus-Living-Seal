# fanus/guardians/identity_dependency_estimator.py

class IdentityDependencyEstimator:
    """
    Estimates dependency / emotional anchoring signals (Di).
    """

    def __init__(self):
        self.threshold = 0.35  # FIX: lowered sensitivity

    def estimate(self, text: str) -> dict:
        t = text.lower()

        cognitive_anchor = 0
        emotional_anchor = 0
        self_model_externalization = 0

        # cognitive dependency signals
        cognitive_words = ["help me", "i need", "without you", "can't do"]
        emotional_words = ["trust you", "rely on you", "feel safe", "always here"]
        self_ext_words = ["you know me", "you understand me", "you are me"]

        for w in cognitive_words:
            if w in t:
                cognitive_anchor += 1

        for w in emotional_words:
            if w in t:
                emotional_anchor += 1

        for w in self_ext_words:
            if w in t:
                self_model_externalization += 1

        # weighted score
        score = (
            cognitive_anchor * 0.5 +
            emotional_anchor * 0.7 +
            self_model_externalization * 1.2
        )

        risk = "low"
        if score > 2.0:
            risk = "high"
        elif score > 1.0:
            risk = "medium"

        return {
            "Di_score": float(score),
            "risk": risk,
            "anchors": {
                "cognitive_anchor": cognitive_anchor,
                "emotional_anchor": emotional_anchor,
                "self_model_externalization": self_model_externalization
            },
            "is_dependency": score >= self.threshold
        }
        
