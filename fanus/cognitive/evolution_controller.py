class FanusEvolutionController:

    def __init__(self):

        self.history_patterns = {}
        self.evolution_log = []

    # =========================
    # 🧠 MAIN ENTRY
    # =========================
    def evaluate(self, memory_snapshot, meta_result):

        proposals = []

        intent_dist = memory_snapshot.get("intent_distribution", {})

        stability = meta_result.get("stability", 0)

        # -------------------------
        # 📊 PATTERN DETECTION
        # -------------------------
        most_common_intent = self._get_most_common(intent_dist)

        # -------------------------
        # 🔥 EVOLUTION RULES
        # -------------------------

        # Rule 1: instability
        if stability < 0.5:
            proposals.append({
                "type": "stability_repair",
                "action": "increase_stability_bias",
                "reason": "low system stability detected"
            })

        # Rule 2: repetitive behavior
        if intent_dist.get(most_common_intent, 0) > 3:
            proposals.append({
                "type": "diversity_boost",
                "action": "increase_exploration",
                "reason": "repetitive intent detected"
            })

        # Rule 3: healthy system
        if stability > 0.7:
            proposals.append({
                "type": "optimization",
                "action": "optimize_decision_speed",
                "reason": "system stable enough for optimization"
            })

        return {
            "most_common_intent": most_common_intent,
            "proposals": proposals
        }

    # =========================
    # 📊 ANALYSIS HELPERS
    # =========================
    def _get_most_common(self, intent_dist):

        if not intent_dist:
            return None

        return max(intent_dist, key=intent_dist.get)
