cat > ~/Desktop/Fanus-Living-Seal/fanus-v2/memory/ledger.py << 'EOF'
import json
import os
from datetime import datetime

class Ledger:
    def __init__(self, filepath="ledger.json"):
        self.filepath = filepath
        self.entries = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.entries, f, indent=2)

    def add_entry(self, record: dict):
        record["timestamp"] = datetime.now().isoformat()
        self.entries.append(record)
        self._save()

    def get_last_n(self, n: int = 10):
        return self.entries[-n:] if self.entries else []

    def get_all(self):
        return self.entries.copy()

    def get_last(self):
        return self.entries[-1] if self.entries else None
EOF
