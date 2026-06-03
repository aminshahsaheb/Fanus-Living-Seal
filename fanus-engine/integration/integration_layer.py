class IntegrationLayer:

    def __init__(self, orchestrator, control_center):

        self.orchestrator = orchestrator
        self.control_center = control_center

        # shared system context (حافظه مشترک زنده)
        self.shared_state = {
            "global_confidence": 1.0,
            "system_health": 1.0,
            "drift_history": []
        }

    def step(self, event: dict):

        """
        اینجا نقطه‌ایه که کل سیستم با هم هماهنگ می‌شود
        """

        # ─────────────────────────────
        # 1. ORCHESTRATION STEP
        # ─────────────────────────────
        orchestrator_output = self.orchestrator.tick(event)

        # ─────────────────────────────
        # 2. CONTROL CENTER STEP
        # ─────────────────────────────
        control_output = orchestrator_output["control_output"]

        # ─────────────────────────────
        # 3. DRIFT AGGREGATION
        # ─────────────────────────────
        drift = control_output.get("drift", 0.0)

        self.shared_state["drift_history"].append(drift)

        if len(self.shared_state["drift_history"]) > 50:
            self.shared_state["drift_history"].pop(0)

        # ─────────────────────────────
        # 4. GLOBAL HEALTH CALCULATION
        # ─────────────────────────────
        avg_drift = sum(self.shared_state["drift_history"]) / max(
            1,
            len(self.shared_state["drift_history"])
        )

        self.shared_state["system_health"] = max(0.0, 1.0 - avg_drift)

        # ─────────────────────────────
        # 5. GLOBAL CONFIDENCE SYNC
        # ─────────────────────────────
        state = control_output.get("state", {})

        local_conf = state.get("confidence", 1.0)

        self.shared_state["global_confidence"] = (
            0.7 * local_conf +
            0.3 * self.shared_state["system_health"]
        )

        # ─────────────────────────────
        # 6. BACKPROPAGATION TO CONTROL CENTER
        # ─────────────────────────────
        self.control_center.policy.adjust_global_pressure(
            self.shared_state["system_health"]
        )

        # ─────────────────────────────
        # 7. STABILITY DECISION
        # ─────────────────────────────
        if self.shared_state["system_health"] < 0.3:

            self.control_center.state = "CRITICAL"

        elif self.shared_state["system_health"] < 0.6:

            self.control_center.state = "UNSTABLE"

        else:

            self.control_center.state = "STABLE"

        # ─────────────────────────────
        # 8. FINAL OUTPUT
        # ─────────────────────────────
        return {
            "orchestrator": orchestrator_output,
            "control": control_output,
            "shared_state": self.shared_state
        }
