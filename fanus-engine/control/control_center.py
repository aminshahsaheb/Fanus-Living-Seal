from fanus_engine.control.threshold_policy import ThresholdPolicy
from fanus_engine.control.action_router import ActionRouter
from fanus_engine.control.realignment_engine import RealignmentEngine

from fanus_engine.grounding.external_grounding import ExternalGrounding
from fanus_engine.grounding.reality_adapter import RealityAdapter

from fanus_engine.meta.meta_auditor import MetaAuditor
from fanus_engine.memory.wound_ledger import WoundLedger


class ControlCenter:

    def __init__(self):

        # ─────────────────────────────
        # CORE DECISION MODULES
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
        # MEMORY LAYER (WOUND LEDGER)
        # ─────────────────────────────
        self.wounds = WoundLedger()

    def process(self, drift_result: dict, state: dict, context: dict = None):

        if context is None:
            context = {}

        # ─────────────────────────────
        # 1. EXTRACT DRIFT
        # ─────────────────────────────
        drift = drift_result.get("drift", 0.0)

        # ─────────────────────────────
        # 2. RISK POLICY
        # ─────────────────────────────
        risk = self.policy.evaluate(drift)

        # ─────────────────────────────
        # 3. ROUTING DECISION
        # ─────────────────────────────
        action = self.router.route(risk)

        # ─────────────────────────────
        # 4. REALIGNMENT (internal correction)
        # ─────────────────────────────
        if action == "REALIGN":
            state = self.realigner.apply(state, drift)

        # ─────────────────────────────
        # 5. EXTERNAL REALITY SIGNAL
        # ─────────────────────────────
        external_signal = self.reality.fetch_external_signal(context)

        # ─────────────────────────────
        # 6. GROUNDING CHECK
        # ─────────────────────────────
        grounding_result = self.grounding.evaluate(
            system_output=drift_result,
            external_signal=external_signal
        )

        # ─────────────────────────────
        # 7. WOUND LOGGING (IMPORTANT)
        # ─────────────────────────────
        if grounding_result.get("mismatch", False):

            self.wounds.record(
                wound_type="external_truth_conflict",
                severity=float(drift),
                details={
                    "drift": drift_result,
                    "grounding": grounding_result,
                    "context": context
                }
            )

            state["confidence"] = max(
                0.0,
                state.get("confidence", 1.0)
                - grounding_result.get("confidence_penalty", 0.1)
            )

            state["mode"] = "external_correction_required"

        # ─────────────────────────────
        # 8. BUILD REPORT
        # ─────────────────────────────
        report = {
            "risk": risk,
            "action": action,
            "drift": drift,
            "grounding": grounding_result,
            "state": state,
            "wounds_count": self.wounds.count(),
            "recent_wounds": self.wounds.recent(3)
        }

        # ─────────────────────────────
        # 9. META AUDIT
        # ─────────────────────────────
        meta_report = self.meta.audit(report)
        report["meta"] = meta_report

        # ─────────────────────────────
        # 10. FINAL OUTPUT
        # ─────────────────────────────
        return report
