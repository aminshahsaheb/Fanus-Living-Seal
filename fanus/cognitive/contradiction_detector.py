import time


class ContradictionDetector:

    def __init__(self):
        self.contradictions = []

    def check(self, claim_a, claim_b, source_a="unknown", source_b="unknown"):
        keywords_a = set(claim_a.lower().split())
        keywords_b = set(claim_b.lower().split())
        overlap = keywords_a & keywords_b
        negations = ["نیست", "نه", "نمی", "بدون", "فاقد", "not", "no", "never"]
        has_negation = any(n in claim_a.lower() or n in claim_b.lower() for n in negations)
        is_contradiction = len(overlap) > 1 and has_negation
        result = {
            "claim_a": claim_a,
            "claim_b": claim_b,
            "source_a": source_a,
            "source_b": source_b,
            "overlap_keywords": list(overlap),
            "is_contradiction": is_contradiction,
            "confidence": 0.8 if is_contradiction else 0.2,
            "timestamp": time.time()
        }
        if is_contradiction:
            self.contradictions.append(result)
        return result

    def get_all(self):
        return self.contradictions

    def stats(self):
        return {"total_checked": len(self.contradictions), "contradictions": len(self.contradictions)}