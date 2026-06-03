from fanus_engine.wound.wound_engine import WoundEngine
from fanus_engine.wound.wound_ledger import WoundLedger


class DriftEngine:

    def __init__(self):
        # Wound system integration
        self.wound_engine = WoundEngine(WoundLedger())

        # weights (tunable in v2.1 later)
        self.w_epistemic = 0.30
        self.w_narrative = 0.25
        self.w_compression = 0.15
        self.w_alignment = 0.30

    def compute(self, epistemic, narrative, compression, alignment):
        """
        V2 Drift computation + Wound registration
        """

        # ─────────────────────────────
        # 1. BASE DRIFT
        # ─────────────────────────────
        drift = (
            self.w_epistemic * epistemic +
            self.w_narrative * narrative +
            self.w_compression * compression +
            self.w_alignment * (1 - alignment)
        )

        # ─────────────────────────────
        # 2. RISK CLASSIFICATION
        # ─────────────────────────────
        if drift < 0.3:
            risk = "STABLE"
        elif drift < 0.6:
            risk = "WATCH"
        elif drift < 0.8:
            risk = "HIGH"
        else:
            risk = "CRITICAL"

        # ─────────────────────────────
        # 3. WOUND REGISTRATION (IMPORTANT)
        # ─────────────────────────────
        if drift > 0.6:
            self.wound_engine.record_drift_spike(
                drift_score=drift,
                context={
                    "epistemic": epistemic,
                    "narrative": narrative,
                    "compression": compression,
                    "alignment": alignment,
                    "risk": risk
                }
            )

        # ─────────────────────────────
        # 4. OUTPUT STRUCTURE
        # ─────────────────────────────
        return {
            "drift": drift,
            "risk": risk,
            "action": self._decide_action(risk)
        }

    def _decide_action(self, risk):
        """
        Control signal for next layer
        """

        if risk == "STABLE":
            return "CONTINUE"

        if risk == "WATCH":
            return "LOG_ONLY"

        if risk == "HIGH":
            return "REALIGN"

        if risk == "CRITICAL":
            return "HALT_AND_AUDIT"
