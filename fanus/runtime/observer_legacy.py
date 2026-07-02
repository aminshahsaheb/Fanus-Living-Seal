class FanusObserver:

    def __init__(self):
        self.history = []
        self.stats = {
            "total_ticks": 0,
            "allow_count": 0,
            "caution_count": 0
        }

    # =========================
    # 👁 OBSERVE RESULT
    # =========================
    def observe(self, result):

        self.history.append(result)
        self.stats["total_ticks"] += 1

        decision = result.get("decision")

        if decision == "ALLOW":
            self.stats["allow_count"] += 1

        if decision == "ALLOW_WITH_CAUTION":
            self.stats["caution_count"] += 1

        return self._analyze()

    # =========================
    # 🧠 ANALYSIS CORE
    # =========================
    def _analyze(self):

        total = self.stats["total_ticks"]
        allow = self.stats["allow_count"]
        caution = self.stats["caution_count"]

        stability = 1.0

        if total > 0:
            stability = allow / total

        return {
            "stability_score": round(stability, 3),
            "total_ticks": total,
            "allow_ratio": allow,
            "caution_ratio": caution
        }
