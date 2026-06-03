from fanus_engine.control.threshold_policy import ThresholdPolicy
from fanus_engine.control.action_router import ActionRouter
from fanus_engine.control.realignment_engine import RealignmentEngine

from fanus_engine.grounding.external_grounding import ExternalGrounding
from fanus_engine.grounding.reality_adapter import RealityAdapter

from fanus_engine.meta.meta_auditor import MetaAuditor

from fanus_engine.memory.wound_ledger import WoundLedger
from fanus_engine.memory.scar_engine import ScarEngine

from fanus_engine.control.adaptive_policy_engine import AdaptivePolicyEngine


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
        # META LAYER
        # ─────────────────────────────
        self.meta = MetaAuditor()

        # ─────────────────────────────
        # MEMORY LAYER
        # ─────────────────────────────
        self.wounds = WoundLedger()
        self.scar_engine = ScarEngine(threshold=3)

        # ─────────────────────────────
        # ADAPTIVE POLICY LAYER (V2.4)
        # ─────────────────────────────
        self.adaptive_policy = AdaptivePolicyEngine()

    def process(self, drift_result: dict, state: dict, context: dict = None):

        if context is None:
            context = {}

        # ─────────────────────────────
        # 1. DRIFT EXTRACTION
        # ─────────────────────────────
        drift = drift_result.get("drift", 0.0)

        # ─────────────────────────────
        # 2. POLICY EVALUATION
        # ─────────────────────────────
        risk = self.policy.evaluate(drift)

        # ─────────────────────────────
        # 3. ACTION ROUTING
        # ─────────────────────────────
        action = self.router.route(risk)

        # ─────────────────────────────
        # 4. REALIGNMENT
        # ─────────────────────────────
        if action == "REALIGN":
            state = self.realigner.apply(state, drift)

        # ─────────────────────────────
        # 5. EXTERNAL REALITY CHECK
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
                "details": {
                    "drift": drift_result,
                    "grounding": grounding_result,
                    "context": context
                }
            }

            # SAVE WOUND
            self.wounds.record(
                wound_type=wound["wound_type"],
                severity=wound["severity"],
                details=wound["details"]
            )

            # FEED SCAR ENGINE
            self.scar_engine.ingest_wound(wound)

            # CONFIDENCE UPDATE
            state["confidence"] = max(
                0.0,
                state.get("confidence", 1.0)
                - grounding_result.get("confidence_penalty", 0.1)
            )

            state["mode"] = "external_correction_required"

        # ─────────────────────────────
        # 7. ADAPTIVE POLICY UPDATE (V2.4 CORE)
        # ─────────────────────────────
        self.adaptive_policy.update_from_scars(
            self.scar_engine.get_active_scars()
        )

        # ─────────────────────────────
        # 8. FINAL REPORT
        # ─────────────────────────────
        report = {
            "risk": risk,
            "action": action,
            "drift": drift,
            "grounding": grounding_result,
            "state": state,

            "wounds_count": self.wounds.count(),
            "recent_wounds": self.wounds.recent(3),

            "scars": self.scar_engine.get_active_scars(),

            "policy": self.adaptive_policy.get_policy()
        }

        # ─────────────────────────────
        # 9. META AUDIT
        # ─────────────────────────────
        report["meta"] = self.meta.audit(report)

        return report
