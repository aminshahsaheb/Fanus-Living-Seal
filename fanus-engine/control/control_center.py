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
        # CORE CONTROL
        # ─────────────────────────────
        self.policy = ThresholdPolicy()
        self.router = ActionRouter()
        self.realigner = RealignmentEngine()

        # ─────────────────────────────
        # EXTERNAL GROUNDING
        # ─────────────────────────────
        self.grounding = ExternalGrounding()
        self.reality = RealityAdapter()

        # ─────────────────────────────
        # META LAYERS
        # ─────────────────────────────
        self.identity = SystemIdentity()
        self.trust = TrustEngine()
        self.boundary = AutonomyBoundary()
        self.closure = ClosureManager()

    # ─────────────────────────────
    # MAIN PIPELINE
    # ─────────────────────────────
    def process(self, drift_result: dict, state: dict, context: dict = None):

        if context is None:
            context = {}

        # ─────────────────────────────
        # 1. DRIFT CORE SIGNAL
        # ─────────────────────────────
        drift = float(drift_result.get("drift", 0.0))

        # ─────────────────────────────
        # 2. IDENTITY VALIDATION
        # ─────────────────────────────
        identity = self.identity.evaluate(state, context)

        # ─────────────────────────────
        # 3. TRUST EVOLUTION
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
        # 5. BOUNDARY FILTER
        # ─────────────────────────────
        boundary = self.boundary.check_action(
            action=action,
            drift=drift,
            trust=trust
        )

        if not boundary["allowed"]:
            action = "BLOCKED_BY_BOUNDARY"

        # ─────────────────────────────
        # 6. REALIGNMENT (if needed)
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
        # 8. CLOSURE EVALUATION
        # ─────────────────────────────
        closure = self.closure.evaluate_system(
            stability_score=(1.0 - drift),
            rewrite_requests=state.get("rewrite_requests", 0)
        )

        # ─────────────────────────────
        # 9. GLOBAL SAFETY ADJUSTMENT
        # ─────────────────────────────
        if grounding.get("mismatch", False):

            state["confidence"] = max(
                0.0,
                state.get("confidence", 1.0) - grounding.get("confidence_penalty", 0.1)
            )

            state["mode"] = "external_correction_required"

        # ─────────────────────────────
        # 10. SYSTEM FREEZE IF CLOSED
        # ─────────────────────────────
        if closure["is_closed"]:
            state["mode"] = "locked_stable_state"

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
