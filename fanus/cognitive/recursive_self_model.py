class FanusRecursiveSelfModel:

    def __init__(self):

        self.levels = []
        self.recursion_depth = 0

    # =========================
    # 🧠 MAIN ENTRY
    # =========================
    def update(self, self_model, meta_model, memory_snapshot):

        base = {
            "self_model": self_model,
            "meta_model": meta_model,
            "memory": memory_snapshot
        }

        self.levels.append(base)

        if len(self.levels) > 20:
            self.levels.pop(0)

        return self._build_recursive_view()

    # =========================
    # 🔁 RECURSIVE BUILD
    # =========================
    def _build_recursive_view(self):

        depth = len(self.levels)

        self.recursion_depth = depth

        # Layer 1: current state
        current = self.levels[-1]

        # Layer 2: aggregated view
        aggregated = self._aggregate()

        # Layer 3: meta-recursive insight
        recursive_insight = {
            "depth": depth,
            "stability_trend": self._compute_stability_trend(),
            "identity_coherence": self._compute_coherence()
        }

        return {
            "current_state": current,
            "aggregated_state": aggregated,
            "recursive_insight": recursive_insight
        }

    # =========================
    # 📊 ANALYSIS
    # =========================
    def _aggregate(self):

        total = len(self.levels)

        if total == 0:
            return {}

        avg_stability = 0.0

        for l in self.levels:
            meta = l.get("meta_model", {})
            avg_stability += meta.get("stability", 0)

        avg_stability /= total

        return {
            "avg_stability": round(avg_stability, 3),
            "samples": total
        }

    # =========================
    # 📈 TREND
    # =========================
    def _compute_stability_trend(self):

        values = []

        for l in self.levels:
            meta = l.get("meta_model", {})
            values.append(meta.get("stability", 0))

        if len(values) < 2:
            return "stable"

        if values[-1] > values[0]:
            return "improving"

        if values[-1] < values[0]:
            return "declining"

        return "stable"

    # =========================
    # 🧠 COHERENCE
    # =========================
    def _compute_coherence(self):

        if len(self.levels) < 3:
            return 1.0

        changes = 0

        for i in range(1, len(self.levels)):

            prev = self.levels[i-1].get("self_model", {})
            curr = self.levels[i].get("self_model", {})

            if prev != curr:
                changes += 1

        coherence = 1 - (changes / len(self.levels))

        return round(coherence, 3)
