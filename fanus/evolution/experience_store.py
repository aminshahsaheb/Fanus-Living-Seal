import json
import os
from datetime import datetime

class ExperienceStore:

    def __init__(self, path="fanus_memory.json"):
        self.path = path

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def load_all(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return []

    def store(self, entry):
        data = self.load_all()

        entry["timestamp"] = str(datetime.now())

        data.append(entry)

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def find_by_intent(self, intent):
        data = self.load_all()
        return [d for d in data if d.get("intent") == intent]
