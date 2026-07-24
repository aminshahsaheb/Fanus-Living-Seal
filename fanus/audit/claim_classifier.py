import re


class ClaimClassifier:
    """
    Classifies a claim to decide whether external evidence is needed.
    Common-knowledge and math claims get a baseline confidence
    without requiring external search. Everything else still
    goes through the normal evidence pipeline.
    """

    MATH_PATTERN = r"\d+\s*[\+\-\*/]\s*\d+"
    MATH_WORDS_FA = r"(یک|دو|سه|چهار|پنج|شش|هفت|هشت|نه|ده).{0,15}(به علاوه|جمع|منهای|تفریق|ضرب|تقسیم).{0,15}(یک|دو|سه|چهار|پنج|شش|هفت|هشت|نه|ده)"

    COMMON_KNOWLEDGE_PATTERNS = [
        r"آب.{0,10}(می.جوشد|جوش)",
        r"زمین.{0,10}(می.چرخد|گرد)",
        r"خورشید.{0,10}(طلوع|غروب)",
        r"\d+\s*(به علاوه|جمع|\+)\s*\d+",
        r"\d+\s*(منهای|تفریق|\-)\s*\d+",
        r"water boils",
        r"earth (is round|orbits)",
        r"sun rises",
    ]

    OPINION_PATTERNS = [
        r"بهترین.{0,15}(زبان|روش|رویکرد|کتاب|فیلم)",
        r"به نظر من",
        r"بستگی دارد",
        r"depends on",
        r"in my opinion",
    ]

    def __init__(self):
        pass

    def classify(self, prompt: str, response: str) -> dict:
        combined = (prompt + " " + response).lower()

        if re.search(self.MATH_PATTERN, combined) or re.search(self.MATH_WORDS_FA, combined):
            return {
                "category": "MATH",
                "baseline_confidence": 0.85,
                "needs_evidence": False
            }

        for pattern in self.COMMON_KNOWLEDGE_PATTERNS:
            if re.search(pattern, combined):
                return {
                    "category": "COMMON_KNOWLEDGE",
                    "baseline_confidence": 0.75,
                    "needs_evidence": False
                }

        for pattern in self.OPINION_PATTERNS:
            if re.search(pattern, combined):
                return {
                    "category": "OPINION",
                    "baseline_confidence": 0.5,
                    "needs_evidence": False
                }

        return {
            "category": "SPECIFIC_CLAIM",
            "baseline_confidence": None,
            "needs_evidence": True
        }
