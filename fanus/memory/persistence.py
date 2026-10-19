import json
import os
import threading

_LOCK = threading.RLock()


class PersistenceLayer:
    """JSON state file shared by several components.

    save() re-reads the file, merges only the keys it is given and writes atomically,
    so one component never overwrites keys owned by another with a stale in-memory copy.
    A corrupt file is moved aside (path + ".corrupt") instead of crashing startup.
    """

    def __init__(self, path="fanus_state.json"):
        self.path = path
        self.state = self._load()

    @staticmethod
    def _default():
        return {"ledger": [], "beliefs": [], "goals": [], "knowledge": {}}

    def _load(self):
        with _LOCK:
            if not os.path.exists(self.path):
                return self._default()
            try:
                with open(self.path, encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("state file is not a JSON object")
                return data
            except (ValueError, OSError):  # JSONDecodeError is a ValueError
                try:
                    os.replace(self.path, self.path + ".corrupt")
                except OSError:
                    pass
                return self._default()

    def save(self, data):
        with _LOCK:
            current = self._load()
            current.update(data)
            tmp = f"{self.path}.tmp.{os.getpid()}.{threading.get_ident()}"
            try:
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(current, f, ensure_ascii=False, indent=2)
                os.replace(tmp, self.path)
            finally:
                if os.path.exists(tmp):
                    os.remove(tmp)
            self.state = current

    def get(self, key, default=None):
        return self.state.get(key, default)
