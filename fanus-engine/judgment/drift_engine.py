from fanus_engine.wound.wound_engine import WoundEngine
from fanus_engine.wound.wound_ledger import WoundLedger
from fanus_engine.learning.parameter_store import ParameterStore


class DriftEngine:

    def __init__(self):

        # ─────────────────────────────
        # SYSTEM COMPONENTS
        # ─────────────────────────────
        self.wound_engine = WoundEngine(WoundLedger())
        self.params = ParameterStore()

    def compute(self, epistemic, narrative, compression, alignment):

        # ─────────────────────────────
        # LOAD DYNAMIC WEIGHTS (SELF-LEARNING)
        # ─────────────────────────────
        w = self.params.weights

        # ─────────────────────────────
        # BASE DRIFT CALCULATION
        # ─────────────────────────────
        drift = (
            w["epistemic"] * epistemic +
            w["narrative"] * narrative +
            w["compression"] * compression +
            w["alignment"] * (1 - alignment)
        )

        # ─────────────────────────────
        # RISK LEVEL
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
        # WOUND REGISTRATION
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
        # ACTION POLICY
        # ─────────────────────────────
        action = self._decide_action(risk)

        return {
            "drift": drift,
            "risk": risk,
            "action": action
        }

    def _decide_action(self, risk):

        if risk == "STABLE":
            return "CONTINUE"

        if risk == "WATCH":
            return "LOG_ONLY"

        if risk == "HIGH":
            return "REALIGN"

        if risk == "CRITICAL":
            return "HALT_AND_AUDIT"
