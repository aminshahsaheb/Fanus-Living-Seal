import time


class MemoryLedger:

    def __init__(self):
        self.ledger = []

    def record(self, source, content, confidence=1.0):
        event = {
            "id": len(self.ledger) + 1,
            "timestamp": time.time(),
            "source": source,
            "content": content,
            "confidence": confidence,
            "verified": False
        }
        self.ledger.append(event)
        return event

    def verify(self, event_id):
        for e in self.ledger:
            if e["id"] == event_id:
                e["verified"] = True
                return e
        return None

    def get_verified(self):
        return [e for e in self.ledger if e["verified"]]

    def get_all(self):
        return self.ledger

    def size(self):
        return len(self.ledger)