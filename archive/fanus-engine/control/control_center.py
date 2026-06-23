from fanus_engine.control.threshold_policy import ThresholdPolicy
from fanus_engine.control.action_router import ActionRouter
from fanus_engine.control.realignment_engine import RealignmentEngine

from fanus_engine.grounding.external_grounding import ExternalGrounding
from fanus_engine.grounding.reality_adapter import RealityAdapter

from fanus_engine.identity.system_identity import SystemIdentity
from fanus_engine.trust_layer.trust_engine import TrustEngine
from fanus_engine.governance.autonomy_boundary import AutonomyBoundary
from fanus_engine.closure.closure_manager import ClosureManager


class ControlCenter:

    def __init__(self):

        # ─────────────────────────────
        # CORE DECISION LAYER
        # ─────────────────────────────
        self.policy = ThresholdPolicy()
        self.router = ActionRouter()
        self.realigner = RealignmentEngine()

        # ─────────────────────────────
        # GROUNDING LAYER
        # ─────────────────────────────
        self.grounding = ExternalGrounding()
        self.reality = RealityAdapter()

        # ─────────────────────────────
        # META COGNITIVE LAYERS
        # ─────────────────────────────
        self.identity = SystemIdentity()
        self.trust = TrustEngine()
        self.boundary = AutonomyBoundary()
        self.closure = ClosureManager()

    # ─────────────────────────────
    # MAIN PROCESS PIPELINE
    # ─────────────────────────────
    def process(self, drift_result: dict, state: dict, context: dict = None):

        if context is None:
            context = {}

        # ─────────────────────────────
        # 1. DRIFT SIGNAL
        # ─────────────────────────────
        drift = float(drift_result.get("drift", 0.0))

        # ─────────────────────────────
        # 2. IDENTITY EVALUATION
        # ─────────────────────────────
        identity = self.identity.evaluate(state, context)

        # ─────────────────────────────
        # 3. TRUST UPDATE (stateful)
        # ─────────────────────────────
        trust = self.trust.update(
            output=drift_result,
            state=state,
            identity=identity
        )

        # ─────────────────────────────
        # 4. POLICY DECISION
        # ─────────────────────────────
        risk = self.policy.evaluate(drift)
        action = self.router.route(risk)

        # ─────────────────────────────
        # 5. AUTONOMY BOUNDARY CHECK
        # ─────────────────────────────
        boundary = self.boundary.check_action(
            action=action,
            drift=drift,
            trust=trust
        )

        if not boundary["allowed"]:
            action = "BLOCKED_BY_BOUNDARY"

        # ─────────────────────────────
        # 6. REALIGNMENT (if allowed)
        # ─────────────────────────────
        if action == "REALIGN":
            state = self.realigner.apply(state, drift)

        # ─────────────────────────────
        # 7. REALITY GROUNDING
        # ─────────────────────────────
        external_signal = self.reality.fetch_external_signal(context)

        grounding = self.grounding.evaluate(
            system_output=drift_result,
            external_signal=external_signal
        )

        # ─────────────────────────────
        # 8. CLOSURE LOGIC (STABILITY CONTROL)
        # ─────────────────────────────
        stability_score = 1.0 - drift

        closure = self.closure.evaluate_system(
            stability_score=stability_score,
            rewrite_requests=state.get("rewrite_requests", 0)
        )

        # ─────────────────────────────
        # 9. STATE CORRECTION (REALITY MISMATCH)
        # ─────────────────────────────
        if grounding.get("mismatch", False):

            state["confidence"] = max(
                0.0,
                state.get("confidence", 1.0)
                - grounding.get("confidence_penalty", 0.1)
            )

            state["mode"] = "EXTERNAL_CORRECTION_REQUIRED"

        # ─────────────────────────────
        # 10. LOCK STATE HANDLING
        # ─────────────────────────────
        if closure.get("is_closed", False):
            state["mode"] = "LOCKED_STABLE_STATE"

        # ─────────────────────────────
        # 11. FINAL OUTPUT
        # ─────────────────────────────
        return {
            "drift": drift,
            "risk": risk,
            "action": action,
            "identity": identity,
            "trust": trust,
            "boundary": boundary,
            "grounding": grounding,
            "closure": closure,
            "state": state
        }
