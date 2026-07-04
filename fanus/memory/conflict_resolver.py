import time


class ConflictResolver:

    def __init__(self):
        self.conflicts = []

    def add(self, claim_a, source_a, confidence_a, claim_b, source_b, confidence_b):
        conflict = {
            "claim_a": {"content": claim_a, "source": source_a, "confidence": confidence_a},
            "claim_b": {"content": claim_b, "source": source_b, "confidence": confidence_b},
            "resolved": False,
            "winner": None,
            "timestamp": time.time()
        }
        if abs(confidence_a - confidence_b) > 0.3:
            conflict["resolved"] = True
            conflict["winner"] = claim_a if confidence_a > confidence_b else claim_b
        self.conflicts.append(conflict)
        return conflict

    def get_unresolved(self):
        return [c for c in self.conflicts if not c["resolved"]]

    def stats(self):
        return {
            "total": len(self.conflicts),
            "resolved": len([c for c in self.conflicts if c["resolved"]]),
            "unresolved": len(self.get_unresolved())
        }