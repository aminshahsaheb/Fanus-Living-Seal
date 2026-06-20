class FanusSystemCollapseStabilizer:

    def __init__(self):

        self.alert_level = 0.0
        self.frozen = False
        self.recovery_mode = False

    # =========================
    # 🧠 MAIN CHECK
    # =========================
    def analyze(self, unified_field, boundary, recursive):

        drift = unified_field.get("drift", 0.0)
        stability = unified_field.get("stability", 1.0)
        coherence = unified_field.get("coherence", 1.0)

        recursion_depth = recursive.get("recursive_insight", {}).get("depth", 0)

        # -------------------------
        # ⚠️ COLLAPSE SCORE
        # -------------------------
        collapse_score = 0.0

        collapse_score += drift * 0.5
        collapse_score += (1 - stability) * 0.3
        collapse_score += (1 - coherence) * 0.2

        if recursion_depth > 10:
            collapse_score += 0.2

        collapse_score = min(collapse_score, 1.0)

        self.alert_level = collapse_score

        # -------------------------
        # 🛑 STATE DECISION
        # -------------------------
        if collapse_score > 0.75:
            self.frozen = True
            self.recovery_mode = True
            action = "HARD_FREEZE"

        elif collapse_score > 0.5:
            self.frozen = False
            self.recovery_mode = True
            action = "SOFT_DAMPEN"

        else:
            self.frozen = False
            self.recovery_mode = False
            action = "NORMAL_OPERATION"

        return {
            "collapse_score": round(collapse_score, 3),
            "alert_level": round(self.alert_level, 3),
            "state": action,
            "frozen": self.frozen,
            "recovery_mode": self.recovery_mode
        }
