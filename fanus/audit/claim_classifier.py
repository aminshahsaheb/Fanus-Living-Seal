import re

from fanus.audit.support import ascii_digits, check_arithmetic


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
        r"\d+\s*(منهای|تفریق)\s*\d+",
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

    @staticmethod
    def _is_math_expression(text: str) -> bool:
        """An arithmetic expression, not a range: "2019-2021", "87-90%", "24/7" and "3/4" are not subtraction or division."""
        t = ascii_digits(text)
        for m in re.finditer(r"(?<![\w./-])(\d+(?:\.\d+)?)(\s*)([+\-*/×÷])(\s*)(\d+(?:\.\d+)?)(?!\w|[/-]|\.\d)", t):
            a, before, op, after, b = m.groups()
            rest = t[m.end():m.end() + 12]
            if re.match(r"\s*(%|٪|درصد|percent|سال|years?)", rest):
                continue
            if op in "-/":
                if not ((before and after) or re.match(r"\s*=", rest)):
                    continue
                if op == "-" and len(a) == 4 and len(b) == 4:
                    continue
            return True
        return False

    def __init__(self):
        pass

    def classify(self, prompt: str, response: str) -> dict:
        combined = (prompt + " " + response).lower()

        arithmetic = check_arithmetic(response)  # equations in the RESPONSE only; a response may correct the prompt
        if arithmetic is not None or self._is_math_expression(combined) or re.search(self.MATH_WORDS_FA, combined):
            return {
                "category": "MATH",
                "baseline_confidence": 0.85,
                "needs_evidence": False,
                "arithmetic": arithmetic
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
