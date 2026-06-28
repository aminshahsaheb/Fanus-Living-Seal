class CollapseStabilizer:
    """
    SAFETY MONITOR ONLY

    This module does NOT control the system.
    It only observes risk signals and reports collapse probability.
    """

    def __init__(self):
        self.history = []

    # -----------------------------
    # INPUT: unified state snapshot
    # -----------------------------
    def evaluate(self, identity_state: dict, evolution_state: dict):
        identity_stability = identity_state.get("stability", 1.0)

        proposals = evolution_state.get("proposals", [])

        # -----------------------------
        # collapse scoring logic
        # -----------------------------
        collapse_score = 0.0

        # instability factor
        collapse_score += (1.0 - identity_stability) * 0.4

        # aggressive evolution pressure
        if len(proposals) > 2:
            collapse_score += 0.2

        # instability mode penalty
        if identity_state.get("mode") == "adaptive_instability_mode":
            collapse_score += 0.2

        # clamp 0–1
        collapse_score = max(0.0, min(1.0, collapse_score))

        # -----------------------------
        # alert level mapping
        # -----------------------------
        if collapse_score < 0.3:
            alert_level = "LOW"
        elif collapse_score < 0.6:
            alert_level = "MEDIUM"
        else:
            alert_level = "HIGH"

        result = {
            "collapse_score": round(collapse_score, 3),
            "alert_level": alert_level,
            "state": "MONITORING_ONLY",
            "frozen": False,
            "recovery_mode": collapse_score > 0.8
        }

        self.history.append(result)
        return result
