import time


class KnowledgeVersioning:

    def __init__(self):
        self.store = {}

    def add(self, key, content, confidence=1.0):
        if key not in self.store:
            self.store[key] = []
        version = len(self.store[key]) + 1
        entry = {
            "version": version,
            "content": content,
            "confidence": confidence,
            "timestamp": time.time()
        }
        self.store[key].append(entry)
        return entry

    def latest(self, key):
        if key not in self.store:
            return None
        return self.store[key][-1]

    def history(self, key):
        return self.store.get(key, [])

    def all_keys(self):
        return list(self.store.keys())