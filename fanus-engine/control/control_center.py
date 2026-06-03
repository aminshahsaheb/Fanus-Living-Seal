# fanus-engine/control/control_center.py

from fanus_engine.control.threshold_policy import ThresholdPolicy
from fanus_engine.control.action_router import ActionRouter
from fanus_engine.control.realignment_engine import RealignmentEngine


class ControlCenter:

    def __init__(self):
        self.policy = ThresholdPolicy()
        self.router = ActionRouter()
        self.realigner = RealignmentEngine()

    def process(self, drift_result: dict, state: dict):

        drift = drift_result["drift"]

        # ─────────────────────────────
        # 1. classify risk
        # ─────────────────────────────
        risk = self.policy.evaluate(drift)

        # ─────────────────────────────
        # 2. decide action
        # ─────────────────────────────
        action = self.router.route(risk)

        # ─────────────────────────────
        # 3. apply correction if needed
        # ─────────────────────────────
        if action == "REALIGN":
            state = self.realigner.apply(state, drift)

        # ─────────────────────────────
        # 4. final output
        # ─────────────────────────────
        return {
            "risk": risk,
            "action": action,
            "state": state
        }
