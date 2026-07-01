"""
==========================================================
FANUS COLLAPSE SAFETY GATE
==========================================================

Non-authoritative runtime regulator.

ONLY modifies execution intensity, NOT decisions.

==========================================================
"""


class CollapseSafetyGate:

    def __init__(self):

        self.mode = "NORMAL"
        self.cooldown = 0

    # ------------------------------------------

    def evaluate(self, collapse_state: dict):

        collapse_event = collapse_state.get("event", {})
        payload = collapse_event.get("payload", {})

        collapse_score = payload.get("collapse_score", 0.0)
        alert_level = payload.get("alert_level", "LOW")

        # --------------------------------------
        # HIGH RISK
        # --------------------------------------
        if alert_level == "HIGH" or collapse_score > 0.7:

            self.mode = "STABILIZATION"

            return {
                "mode": self.mode,
                "tick_delay": 1.0,
                "execution_limit": True,
                "reason": "high_collapse_pressure"
            }

        # --------------------------------------
        # MEDIUM RISK
        # --------------------------------------
        if alert_level == "MEDIUM" or collapse_score > 0.4:

            self.mode = "CAUTION"

            return {
                "mode": self.mode,
                "tick_delay": 0.5,
                "execution_limit": False,
                "reason": "moderate_collapse_pressure"
            }

        # --------------------------------------
        # NORMAL STATE
        # --------------------------------------
        self.mode = "NORMAL"

        return {
            "mode": self.mode,
            "tick_delay": 0.2,
            "execution_limit": False,
            "reason": "stable_system"
        }
