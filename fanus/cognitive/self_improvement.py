class FanusSelfImprovement:

    def __init__(self):
        self.applied_changes = []
        self.rejected_changes = []

    # =========================
    # 🧠 MAIN ENTRY
    # =========================
    def evaluate(self, meta_result):

        proposals = meta_result.get("proposals", [])

        applied = []

        for p in proposals:
            decision = self._decide(p)

            if decision == "APPLY":
                applied.append(p)
                self.applied_changes.append(p)

            else:
                self.rejected_changes.append(p)

        return {
            "applied": applied,
            "rejected": self.rejected_changes,
            "status": "controlled_evolution_step"
        }

    # =========================
    # ⚖️ DECISION RULES (SAFE MODE)
    # =========================
    def _decide(self, proposal):

        p_type = proposal.get("type")

        # فقط safe rule-based decisions

        if p_type == "warmup":
            return "APPLY"

        if p_type == "stability_fix":
            return "APPLY"

        if p_type == "exploration_boost":
            return "REVIEW"

        return "REVIEW"
