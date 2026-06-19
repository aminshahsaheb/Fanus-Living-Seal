class FanusMemoryLayer:

    def __init__(self, max_size=200):

        self.max_size = max_size
        self.timeline = []

        self.stats = {
            "total_events": 0,
            "intent_map": {}
        }

    # =========================
    # 💾 STORE EVENT
    # =========================
    def store(self, event):

        self.timeline.append(event)
        self.stats["total_events"] += 1

        intent = event.get("intent")

        if intent not in self.stats["intent_map"]:
            self.stats["intent_map"][intent] = 0

        self.stats["intent_map"][intent] += 1

        if len(self.timeline) > self.max_size:
            self.timeline.pop(0)

    # =========================
    # 🔍 GET HISTORY
    # =========================
    def get_history(self):
        return self.timeline

    # =========================
    # 📊 GET SNAPSHOT
    # =========================
    def snapshot(self):

        return {
            "total_events": self.stats["total_events"],
            "intent_distribution": self.stats["intent_map"],
            "memory_size": len(self.timeline)
        }

    # =========================
    # 🧠 SIMPLE PATTERN CHECK
    # =========================
    def pattern(self, intent):

        return self.stats["intent_map"].get(intent, 0)
