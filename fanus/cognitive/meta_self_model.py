class FanusMetaSelfModel:

    def __init__(self):
        self.change_log = []
        self.risk_level = 0.0

    # =========================
    # 🧠 ANALYZE SELF MODEL
    # =========================
    def analyze(self, self_model):

        stability = self_model.get("stability", 0)

        total = self_model.get("total", 0)

        allow = self_model.get("allow", 0)

        caution = self_model.get("caution", 0)

        # -------------------------
        # 📊 RISK CALCULATION
        # -------------------------
        risk = 0.0

        if total > 0:
            caution_ratio = caution / total
            risk = caution_ratio

        if stability < 0.5:
            risk += 0.2

        self.risk_level = min(risk, 1.0)

        return self._propose_changes(self_model)

    # =========================
    # 💡 PROPOSE CHANGES (NO EXECUTION)
    # =========================
    def _propose_changes(self, self_model):

        proposals = []

        if self.risk_level > 0.7:
            proposals.append({
                "type": "stability_fix",
                "action": "reduce_caution_behavior",
                "reason": "high system instability detected"
            })

        if self.risk_level < 0.3:
            proposals.append({
                "type": "exploration_boost",
                "action": "increase_decision_freedom",
                "reason": "system is stable enough for expansion"
            })

        if self_model.get("total", 0) < 5:
            proposals.append({
                "type": "warmup",
                "action": "collect_more_data",
                "reason": "insufficient experience"
            })

        return {
            "risk_level": round(self.risk_level, 3),
            "proposals": proposals
        }
