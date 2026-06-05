import json
import os
from datetime import datetime

class StateStore:
    def __init__(self, filepath="state.json"):
        self.filepath = filepath
        self.state = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.state, f, indent=2)

    def update(self, key, value):
        self.state[key] = value
        self._save()

    def get(self, key, default=None):
        return self.state.get(key, default)

    def get_all(self):
        return self.state.copy()
        
