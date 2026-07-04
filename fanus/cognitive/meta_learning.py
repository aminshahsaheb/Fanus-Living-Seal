import time
from fanus.memory.persistence import PersistenceLayer


class MetaLearning:

    def __init__(self):
        self.persistence = PersistenceLayer()
        self.patterns = self.persistence.get("meta_patterns", [])

    def learn(self, event_type, outcome, context=""):
        pattern = {
            "id": len(self.patterns) + 1,
            "event_type": event_type,
            "outcome": outcome,
            "context": context,
            "reinforcement": 1.0,
            "timestamp": time.time()
        }
        existing = [p for p in self.patterns if p["event_type"] == event_type]
        if existing:
            existing[-1]["reinforcement"] = round(existing[-1]["reinforcement"] * 1.1, 3)
        self.patterns.append(pattern)
        self._save()
        return pattern

    def best_pattern(self, event_type):
        matching = [p for p in self.patterns if p["event_type"] == event_type]
        if not matching:
            return None
        return max(matching, key=lambda p: p["reinforcement"])

    def _save(self):
        self.persistence.save({"meta_patterns": self.patterns})

    def stats(self):
        return {
            "total_patterns": len(self.patterns),
            "event_types": list(set(p["event_type"] for p in self.patterns))
        }