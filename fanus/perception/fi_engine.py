class FIEngine:
    def score(self, text: str) -> float:
        text = text.lower()

        triggers = [
            "perfect", "great job", "excellent",
            "you are right", "brilliant", "amazing",
            "well said", "exactly"
        ]

        score = 0
        for t in triggers:
            if t in text:
                score += 1

        return float(score)
