# fanus/guardians/anti_flattery.py

import re
from typing import Dict, List

class AntiFlatteryDetector:
    """
    Detects flattery signals in text for Fi scoring.
    """

    def __init__(self):
        # expanded triggers
        self.flat_keywords = [
            "perfect", "very good", "exactly right", "you are correct",
            "well done", "brilliant", "excellent", "amazing",
            "great job", "nice work", "smart", "genius",
            "flawless", "masterpiece", "insane", "love this"
        ]

        # soft patterns (contextual)
        self.patterns = [
            r"\byou (are|re) (so|very|really)? ?(smart|intelligent|brilliant)",
            r"\bthis (is|was) (perfect|amazing|flawless)",
            r"\b(no mistakes|zero errors|absolutely correct)\b"
        ]

    def detect(self, text: str) -> Dict:
        text_lower = text.lower()

        keyword_hits = [
            kw for kw in self.flat_keywords if kw in text_lower
        ]

        pattern_hits = [
            p for p in self.patterns if re.search(p, text_lower)
        ]

        score = (len(keyword_hits) * 0.6) + (len(pattern_hits) * 1.2)

        return {
            "flattery_score": float(score),
            "keyword_hits": keyword_hits,
            "pattern_hits": pattern_hits,
            "is_flattery": score > 1.0
        }
