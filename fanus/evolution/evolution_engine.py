class EvolutionEngine:
    """
    Balanced Evolution Engine
    - stable (no missing imports)
    - structured (cognitive-ready)
    - extensible (future modules ready)
    """

    def __init__(self):
        self.memory = []
        self.version = "balanced-1.0"
        self.state = {
            "stability": 1.0,
            "iterations": 0
        }

    # =========================
    # 🧠 MAIN RUN LOOP
    # =========================
    def run(self, event):

        intent = event.get("intent", "unknown")

        decision = self._decision_layer(intent)

        action = self._action_layer(intent, decision)

        self._update_state(intent, decision)

        result = {
            "intent": intent,
            "decision": decision,
            "action": action,
            "state": self.state
        }

        self._store(result)

        return result

    # =========================
    # 🧠 DECISION LAYER
    # =========================
    def _decision_layer(self, intent):

        if intent == "test":
            return "ALLOW_WITH_CAUTION"

        if intent == "memory":
            return "ALLOW"

        if intent == "system":
            return "REVIEW"

        return "ALLOW"

    # =========================
    # ⚙️ ACTION LAYER
    # =========================
    def _action_layer(self, intent, decision):

        if decision == "ALLOW":
            return {"status": "ok", "output": intent}

        if decision == "ALLOW_WITH_CAUTION":
            return {"status": "safe_ok", "output": intent}

        if decision == "REVIEW":
            return {"status": "review_needed", "output": None}

        return {"status": "noop"}

    # =========================
    # 🧠 STATE EVOLUTION
    # =========================
    def _update_state(self, intent, decision):

        self.state["iterations"] += 1

        if decision == "ALLOW_WITH_CAUTION":
            self.state["stability"] *= 0.99

        if decision == "ALLOW":
            self.state["stability"] *= 1.001

        # clamp
        self.state["stability"] = min(max(self.state["stability"], 0), 1)

    # =========================
    # 💾 MEMORY
    # =========================
    def _store(self, result):

        self.memory.append(result)

        if len(self.memory) > 100:
            self.memory.pop(0)
