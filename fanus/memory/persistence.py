import json
import os


class PersistenceLayer:

    def __init__(self, path="fanus_state.json"):
        self.path = path
        self.state = self._load()

    def _load(self):
        if os.path.exists(self.path):
            return json.load(open(self.path))
        return {"ledger": [], "beliefs": [], "goals": [], "knowledge": {}}

    def save(self, data):
        self.state.update(data)
        json.dump(self.state, open(self.path, "w"), ensure_ascii=False, indent=2)

    def get(self, key, default=None):
        return self.state.get(key, default)