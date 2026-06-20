class FanusAutonomyGovernor:

    def __init__(self):

        self.autonomy_level = 0.5  # default mid-level
        self.locked = False

        self.rules = {
            "allow_evolution": True,
            "allow_self_improvement": True,
            "allow_execution": True,
            "allow_identity_shift": False  # مهم: identity fixed by default
        }

    # =========================
    # 🧠 MAIN GOVERNANCE CHECK
    # =========================
    def evaluate(self, unified, stability_report, collapse_report):

        stability = unified.get("stability", 1.0)
        drift = unified.get("drift", 0.0)
        collapse = collapse_report.get("collapse_score", 0.0)

        # -------------------------
        # ⚖️ AUTONOMY SCORE
        # -------------------------
        score = 1.0

        score -= drift * 0.4
        score -= (1 - stability) * 0.3
        score -= collapse * 0.5

        score = max(0.0, min(score, 1.0))

        self.autonomy_level = round(score, 3)

        # -------------------------
        # 🔐 GOVERNANCE RULES
        # -------------------------

        if collapse > 0.75:
            self.locked = True
            self.rules["allow_execution"] = False
            self.rules["allow_evolution"] = False

        elif collapse > 0.5:
            self.rules["allow_execution"] = True
            self.rules["allow_evolution"] = False

        else:
            self.locked = False
            self.rules["allow_execution"] = True
            self.rules["allow_evolution"] = True

        # -------------------------
        # 🧠 FINAL GOVERNANCE STATE
        # -------------------------
        return {
            "autonomy_level": self.autonomy_level,
            "locked": self.locked,
            "rules": self.rules.copy()
        }
