from fanus_engine.control.threshold_policy import ThresholdPolicy
from fanus_engine.control.action_router import ActionRouter
from fanus_engine.control.realignment_engine import RealignmentEngine

from fanus_engine.grounding.external_grounding import ExternalGrounding
from fanus_engine.grounding.reality_adapter import RealityAdapter

from fanus_engine.meta.meta_auditor import MetaAuditor

from fanus_engine.memory.wound_ledger import WoundLedger
from fanus_engine.memory.scar_engine import ScarEngine

from fanus_engine.control.adaptive_policy_engine import AdaptivePolicyEngine
from fanus_engine.control.policy_validator import PolicyValidator
from fanus_engine.control.reality_override import RealityOverride


class ControlCenter:

    def __init__(self):

        # ─────────────────────────────
        # CORE DECISION LAYER
        # ─────────────────────────────
        self.policy = ThresholdPolicy()
        self.router = ActionRouter()
        self.realigner = RealignmentEngine()

        # ─────────────────────────────
        # REALITY LAYER
        # ─────────────────────────────
        self.grounding = ExternalGrounding()
        self.reality = RealityAdapter()

        # ─────────────────────────────
        # META LAYER
        # ─────────────────────────────
        self.meta = MetaAuditor()

        # ─────────────────────────────
        # MEMORY LAYER
        # ─────────────────────────────
        self.wounds = WoundLedger()
        self.scar_engine = ScarEngine(threshold=3)

        # ─────────────────────────────
        # ADAPTIVE LAYER
        # ─────────────────────────────
        self.adaptive_policy = AdaptivePolicyEngine()

        # ─────────────────────────────
        # SAFETY GATE (V2.5)
        # ─────────────────────────────
        self.policy_validator = PolicyValidator()

        # ─────────────────────────────
        # REALITY OVERRIDE (V2.6)
        # ─────────────────────────────
        self.reality_override = RealityOverride()

    def process(self, drift_result: dict, state: dict, context: dict = None):

        if context is None:
            context = {}

        # ─────────────────────────────
        # 1. DRIFT EXTRACTION
        # ─────────────────────────────
        drift = drift_result.get("drift", 0.0)

        # ─────────────────────────────
        # 2. RISK EVALUATION
        # ─────────────────────────────
        risk = self.policy.evaluate(drift)

        # ─────────────────────────────
        # 3. ROUTING DECISION
        # ─────────────────────────────
        action = self.router.route(risk)

        # ─────────────────────────────
        # 4. REALIGNMENT
        # ─────────────────────────────
        if action == "REALIGN":
            state = self.realigner.apply(state, drift)

        # ─────────────────────────────
        # 5. EXTERNAL REALITY SIGNAL
        # ─────────────────────────────
        external_signal = self.reality.fetch_external_signal(context)

        grounding_result = self.grounding.evaluate(
            system_output=drift_result,
            external_signal=external_signal
        )

        # ─────────────────────────────
        # 6. WOUND + SCAR PROCESSING
        # ─────────────────────────────
        if grounding_result.get("mismatch", False):

            wound = {
                "wound_type": "external_truth_conflict",
                "severity": float(drift),
                "details": grounding_result
            }

            self.wounds.record(
                wound_type=wound["wound_type"],
                severity=wound["severity"],
                details=wound["details"]
            )

            self.scar_engine.ingest_wound(wound)

            state["confidence"] = max(
                0.0,
                state.get("confidence", 1.0)
                - grounding_result.get("confidence_penalty", 0.1)
            )

            state["mode"] = "external_correction_required"

        # ─────────────────────────────
        # 7. POLICY VALIDATION GATE
        # ─────────────────────────────
        scars = self.scar_engine.get_active_scars()

        validation = self.policy_validator.validate(
            scars,
            self.adaptive_policy.get_policy()
        )

        if validation["allowed"]:
            self.adaptive_policy.update_from_scars(scars)
        else:
            state["policy_state"] = "frozen"
            state["policy_reason"] = validation

        # ─────────────────────────────
        # 8. REALITY OVERRIDE (FINAL SAFETY GATE)
        # ─────────────────────────────
        override_result = self.reality_override.check(
            state,
            external_signal
        )

        if override_result.get("override", False):

            state["mode"] = "HARD_REALITY_CORRECTION"
            state["override_gap"] = override_result["gap"]

            state["confidence"] = min(
                state.get("confidence", 1.0),
                external_signal.get("ground_truth", 1.0)
            )

        # ─────────────────────────────
        # 9. FINAL REPORT
        # ─────────────────────────────
        report = {
            "risk": risk,
            "action": action,
            "drift": drift,
            "grounding": grounding_result,
            "state": state,

            "wounds_count": self.wounds.count(),
            "recent_wounds": self.wounds.recent(3),

            "scars": scars,
            "policy": self.adaptive_policy.get_policy(),

            "policy_validation": validation,
            "reality_override": override_result
        }

        # ─────────────────────────────
        # 10. META AUDIT
        # ─────────────────────────────
        report["meta"] = self.meta.audit(report)

        return report
