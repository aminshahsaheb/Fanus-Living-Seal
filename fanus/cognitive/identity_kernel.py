class FanusIdentityKernel:

    def __init__(self):

        self.identity_state = {
            "name": "Fanus",
            "type": "controlled_cognitive_system",
            "version": "1.0",
            "stability": 1.0
        }

        self.history = []

    # =========================
    # 🧠 UPDATE IDENTITY
    # =========================
    def update(self, memory_snapshot, meta, evolution, execution):

        self.history.append({
            "memory": memory_snapshot,
            "meta": meta,
            "evolution": evolution,
            "execution": execution
        })

        if len(self.history) > 100:
            self.history.pop(0)

        self._recalculate_identity()

        return self.identity_state

    # =========================
    # 🧠 IDENTITY COMPUTATION
    # =========================
    def _recalculate_identity(self):

        total = len(self.history)

        if total == 0:
            return

        stability_values = []

        for h in self.history:
            meta = h.get("meta", {})
            stability_values.append(meta.get("stability", 0))

        avg_stability = sum(stability_values) / len(stability_values)

        # 🧠 CORE IDENTITY UPDATE RULE
        self.identity_state["stability"] = round(avg_stability, 3)

        # 🧠 EVOLUTION TAGGING
        if avg_stability > 0.7:
            self.identity_state["mode"] = "stable_cognitive_entity"

        elif avg_stability < 0.4:
            self.identity_state["mode"] = "adaptive_instability_mode"

        else:
            self.identity_state["mode"] = "balanced_evolution_state"
