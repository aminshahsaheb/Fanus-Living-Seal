import time


class EvidenceEngine:

    def __init__(self):
        self.claims = []

    def evaluate(self, claim, sources):
        total = 0.0
        for s in sources:
            total += s.get("confidence", 0.0)
        avg = round(total / len(sources), 3) if sources else 0.0
        consensus = "HIGH" if avg > 0.8 else "MEDIUM" if avg > 0.5 else "LOW"
        result = {
            "claim": claim,
            "sources": sources,
            "confidence": avg,
            "consensus": consensus,
            "timestamp": time.time(),
            "accepted": avg > 0.5
        }
        self.claims.append(result)
        return result

    def get_accepted(self):
        return [c for c in self.claims if c["accepted"]]

    def size(self):
        return len(self.claims)