class FanusConsciousLoopBoundary:

    def __init__(self):

        self.drift_history = []
        self.last_state = None

    # =========================
    # 🧠 MAIN CHECK
    # =========================
    def analyze(self, tick, result, meta, identity):

        current_state = {
            "tick": tick,
            "decision": result.get("decision"),
            "stability": meta.get("stability", 0),
            "mode": identity.get("mode", "unknown")
        }

        drift = self._detect_drift(current_state)

        self.drift_history.append(drift)

        if len(self.drift_history) > 50:
            self.drift_history.pop(0)

        control_action = self._decide_control(drift)

        self.last_state = current_state

        return {
            "current_state": current_state,
            "drift_score": drift,
            "control_action": control_action
        }

    # =========================
    # 📉 DRIFT DETECTION
    # =========================
    def _detect_drift(self, state):

        if self.last_state is None:
            return 0.0

        drift = 0.0

        # decision instability
        if state["decision"] != self.last_state["decision"]:
            drift += 0.3

        # stability drop
        if state["stability"] < self.last_state["stability"]:
            drift += 0.4

        # mode change
        if state["mode"] != self.last_state["mode"]:
            drift += 0.3

        return round(min(drift, 1.0), 3)

    # =========================
    # 🛑 CONTROL RULES
    # =========================
    def _decide_control(self, drift):

        if drift > 0.7:
            return "HARD_STABILIZE"

        elif drift > 0.4:
            return "SOFT_STABILIZE"

        else:
            return "CONTINUE"
