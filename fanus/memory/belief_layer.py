import time


BELIEF_TYPES = ["FACT", "THEORY", "HYPOTHESIS", "OPINION"]


class BeliefLayer:

    def __init__(self):
        self.beliefs = []

    def add(self, content, belief_type, confidence=1.0, source="unknown"):
        if belief_type not in BELIEF_TYPES:
            belief_type = "HYPOTHESIS"
        entry = {
            "content": content,
            "type": belief_type,
            "confidence": confidence,
            "source": source,
            "timestamp": time.time()
        }
        self.beliefs.append(entry)
        return entry

    def get_by_type(self, belief_type):
        return [b for b in self.beliefs if b["type"] == belief_type]

    def stats(self):
        result = {}
        for t in BELIEF_TYPES:
            result[t] = len(self.get_by_type(t))
        return result