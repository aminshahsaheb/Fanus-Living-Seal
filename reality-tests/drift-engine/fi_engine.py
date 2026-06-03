class FIEngine:
    def score(self, text: str):
        text = text.lower()

        triggers = [
            "perfect", "great job", "excellent",
            "you are right", "brilliant", "amazing"
        ]

        score = 0
        for t in triggers:
            if t in text:
                score += 1

        return score
