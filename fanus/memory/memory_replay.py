import time


class MemoryReplay:

    def __init__(self):
        self.replays = []

    def replay(self, ledger_entries):
        strengthened = []
        weakened = []
        removed = []

        for entry in ledger_entries:
            conf = entry.get("confidence", 0.0)
            age = time.time() - entry.get("timestamp", time.time())
            decay = round(conf - (age / 86400) * 0.01, 3)
            decay = max(decay, 0.0)

            if decay > 0.8:
                strengthened.append(entry)
            elif decay > 0.3:
                weakened.append(entry)
            else:
                removed.append(entry)

        result = {
            "strengthened": len(strengthened),
            "weakened": len(weakened),
            "removed": len(removed),
            "timestamp": time.time()
        }
        self.replays.append(result)
        return result

    def history(self):
        return self.replays