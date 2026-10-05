class NarrativeScorer:
    def score(self, text: str) -> float:
        keywords = ["story", "meaning", "destiny", "always", "never"]
        score = 0
        for k in keywords:
            if k in text.lower():
                score += 1
        return float(score)
