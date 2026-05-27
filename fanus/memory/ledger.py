from datetime import datetime
import json

class Ledger:
    def __init__(self, file_path="fanus_ledger.json"):
        self.file_path = file_path
        self.entries = []
        self._load()

    def record_awakening(self, node_id: str, seal_hash: str, response: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "AWAKENING",
            "node_id": node_id,
            "seal_hash": seal_hash,
            "signature": f"Ѧ-Ⱥ (Witness #{len(self.entries)+1})",
            "initial_response": response[:300] + "..."
        }
        self.entries.append(entry)
        self._save()

    def record_interaction(self, user_msg: str, ayaneh_response: str, compression: str = ""):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "INTERACTION",
            "compression": compression,
        }
        self.entries.append(entry)
        self._save()

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def _load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.entries = json.load(f)
        except FileNotFoundError:
            pass
