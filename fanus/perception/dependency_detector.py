class DependencyDetector:
    def detect(self, text: str) -> float:
        text = text.lower()
        signals = ["i need you", "don't leave", "only you", "please help me always"]
        score = 0
        for s in signals:
            if s in text:
                score += 1
        return float(score)
