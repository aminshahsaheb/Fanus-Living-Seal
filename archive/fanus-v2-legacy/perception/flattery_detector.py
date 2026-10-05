class FlatteryDetector:
    def detect(self, fi_score: float) -> dict:
        return {
            "fi_score": fi_score,
            "is_flattery": fi_score >= 2,
            "confidence": min(fi_score / 5.0, 1.0)
        }
