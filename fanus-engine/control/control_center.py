from fanus_engine.control.threshold_policy import ThresholdPolicy
from fanus_engine.control.action_router import ActionRouter
from fanus_engine.control.realignment_engine import RealignmentEngine

from fanus_engine.grounding.external_grounding import ExternalGrounding
from fanus_engine.grounding.reality_adapter import RealityAdapter


class ControlCenter:

    def __init__(self):

        # ─────────────────────────────
        # CORE DECISION MODULES
        # ─────────────────────────────
        self.policy = ThresholdPolicy()
        self.router = ActionRouter()
        self.realigner = RealignmentEngine()

        # ─────────────────────────────
        # EXTERNAL GROUNDING MODULES
        # ─────────────────────────────
        self.grounding = ExternalGrounding()
        self.reality = RealityAdapter()

    def process(self, drift_result: dict, state: dict, context: dict = None):

        if context is None:
            context = {}

        # ─────────────────────────────
        # 1. EXTRACT DRIFT
        # ─────────────────────────────
        drift = drift_result["drift"]

        # ─────────────────────────────
        # 2. INTERNAL RISK EVALUATION
        # ─────────────────────────────
        risk = self.policy.evaluate(drift)

        # ─────────────────────────────
        # 3. DECISION ROUTING
        # ─────────────────────────────
        action = self.router.route(risk)

        # ─────────────────────────────
        # 4. REALIGNMENT (if needed)
        # ─────────────────────────────
        if action == "REALIGN":
            state = self.realigner.apply(state, drift)

        # ─────────────────────────────
        # 5. EXTERNAL REALITY SIGNAL
        # ─────────────────────────────
        external_signal = self.reality.fetch_external_signal(context)

        # ─────────────────────────────
        # 6. GROUNDING CHECK (ANTI-SELF-DECEPTION)
        # ─────────────────────────────
        grounding_result = self.grounding.evaluate(
            system_output=drift_result,
            external_signal=external_signal
        )

        # ─────────────────────────────
        # 7. APPLY REALITY PENALTY IF MISMATCH
        # ─────────────────────────────
        if grounding_result["mismatch"]:

            state["confidence"] = max(
                0.0,
                state.get("confidence", 1.0) - grounding_result["confidence_penalty"]
            )

            state["mode"] = "external_correction_required"

        # ─────────────────────────────
        # 8. FINAL OUTPUT
        # ─────────────────────────────
        return {
            "risk": risk,
            "action": action,
            "drift": drift,
            "grounding": grounding_result,
            "state": state
        }
