class SystemObserver:

    def __init__(self):

        self.observation_log = []

    def observe(self, orchestrator_state: dict, control_state: dict, shared_state: dict):

        """
        این لایه تصمیم نمی‌گیرد
        فقط سیستم را "می‌بیند"
        """

        snapshot = {
            "orchestrator_mode": orchestrator_state.get("global_state", {}).get("mode"),
            "stability": orchestrator_state.get("global_state", {}).get("stability"),
            "control_mode": control_state.get("state", {}).get("mode"),
            "confidence": shared_state.get("global_confidence"),
            "system_health": shared_state.get("system_health")
        }

        # ─────────────────────────────
        # 1. DETECT SYSTEM TRENDS
        # ─────────────────────────────
        instability_trend = snapshot["system_health"] < 0.5
        low_confidence = snapshot["confidence"] < 0.4

        # ─────────────────────────────
        # 2. CLASSIFY SYSTEM STATE
        # ─────────────────────────────
        if instability_trend and low_confidence:
            system_state = "FRAGILE"

        elif instability_trend:
            system_state = "UNSTABLE"

        else:
            system_state = "STABLE"

        # ─────────────────────────────
        # 3. STORE OBSERVATION
        # ─────────────────────────────
        self.observation_log.append({
            "snapshot": snapshot,
            "classified_state": system_state
        })

        if len(self.observation_log) > 100:
            self.observation_log.pop(0)

        # ─────────────────────────────
        # 4. RETURN META VIEW (NO ACTION)
        # ─────────────────────────────
        return {
            "system_state": system_state,
            "snapshot": snapshot,
            "trend": "declining" if instability_trend else "stable"
        }
