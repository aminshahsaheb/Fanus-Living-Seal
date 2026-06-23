class FanusEvolutionController:

    def __init__(self):
        self.history = []
        self.stability_memory = []
        self.intent_memory = []

    # =========================
    # 🧠 MAIN DECISION ENGINE
    # =========================
    def evaluate(self, memory_snapshot, meta_result):

        stability = meta_result.get("stability", 0.5)
        intent = meta_result.get("intent", None)
        risk = meta_result.get("risk_level", 0.0)

        self.stability_memory.append(stability)
        self.intent_memory.append(intent)

        most_common_intent = self._get_most_common_intent()

        # =========================
        # 🧯 CRITICAL INSTABILITY
        # =========================
        if stability < 0.3:
            decision = {
                "type": "stability_repair",
                "action": "reduce_entropy",
                "reason": "critical instability detected"
            }

        # =========================
        # ⚖️ MODERATE STABILITY
        # =========================
        elif stability < 0.6:
            decision = {
                "type": "exploration_mode",
                "action": "controlled_learning",
                "reason": "moderate stability window"
            }

        # =========================
        # 🧠 STABLE SYSTEM
        # =========================
        else:
            decision = {
                "type": "execution_ready",
                "action": "process_intent",
                "reason": "system stable"
            }

        # =========================
        # 🧠 INTENT OVERRIDE LAYER
        # =========================
        if intent and meta_result.get("intent_confidence", 0) > 0.7:
            decision = {
                "type": "direct_execution",
                "action": "execute_intent",
                "reason": "high confidence intent override"
            }

        # =========================
        # 🧠 FALLBACK SAFE MODE
        # =========================
        if not intent:
            meta_result["intent"] = "neutral_observe"

        # record history
        self.history.append(decision)

        return {
            "most_common_intent": most_common_intent,
            "stability": stability,
            "proposals": [decision]
        }

    # =========================
    # 📊 INTENT ANALYSIS
    # =========================
    def _get_most_common_intent(self):

        if not self.intent_memory:
            return "unknown"

        freq = {}
        for i in self.intent_memory:
            freq[i] = freq.get(i, 0) + 1

        return max(freq, key=freq.get)
