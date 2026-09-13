import json
import os
from datetime import datetime


class WoundLedger:

    def __init__(
        self,
        path="memory/wounds.json"
    ):

        self.path = path

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump([], f)

    def record(
        self,
        wound_type,
        severity,
        details
    ):

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "wound_type": wound_type,
            "severity": severity,
            "details": details
        }

        data = self.load()

        data.append(entry)

        with open(self.path, "w") as f:
            json.dump(
                data,
                f,
                indent=2
            )

    def load(self):

        with open(self.path, "r") as f:
            return json.load(f)

    def count(self):

        return len(self.load())

    def recent(self, n=5):

        return self.load()[-n:]
