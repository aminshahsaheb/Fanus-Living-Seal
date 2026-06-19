class MetaSelfModel:

    def __init__(self):
        self.insights = []

    # =========================
    # 🧠 1. ANALYZE SELF SYSTEM
    # =========================
    def analyze(self, memory, identity, timeline, multi_self):

        analysis = {
            "memory_density": len(memory),
            "identity_stability": identity.get("stability", 0),
            "timeline_size": timeline.get("timeline_length", 0),
            "multi_self_conflict": self._detect_conflict(multi_self)
        }

        return analysis

    # =========================
    # 🧠 2. DETECT SYSTEM BIAS
    # =========================
    def detect_bias(self, analysis):

        biases = []

        if analysis["identity_stability"] < 0.3:
            biases.append("unstable_identity_system")

        if analysis["multi_self_conflict"] > 2:
            biases.append("internal_agent_conflict")

        if analysis["memory_density"] > 50:
            biases.append("over_memory_accumulation")

        return biases

    # =========================
    # 🧠 3. SYSTEM INTERPRETATION
    # =========================
    def interpret(self, analysis, biases):

        interpretation = []

        if "unstable_identity_system" in biases:
            interpretation.append(
                "System lacks stable self-model; decisions may drift."
            )

        if "internal_agent_conflict" in biases:
            interpretation.append(
                "Multiple internal agents disagree frequently; coherence reduced."
            )

        if not biases:
            interpretation.append(
                "System is stable and self-consistent."
            )

        return interpretation

    # =========================
    # 🧠 4. SELF REDESIGN SUGGESTION
    # =========================
    def suggest_redesign(self, analysis, biases):

        suggestions = []

        if "unstable_identity_system" in biases:
            suggestions.append("Increase identity smoothing window")

        if "internal_agent_conflict" in biases:
            suggestions.append("Increase voting weight of analyst self")

        if analysis["memory_density"] > 100:
            suggestions.append("Introduce memory compression layer")

        return suggestions

    # =========================
    # 🧠 5. FULL PIPELINE
    # =========================
    def run(self, memory, identity, timeline, multi_self):

        analysis = self.analyze(memory, identity, timeline, multi_self)

        biases = self.detect_bias(analysis)

        interpretation = self.interpret(analysis, biases)

        redesign = self.suggest_redesign(analysis, biases)

        return {
            "analysis": analysis,
            "biases": biases,
            "interpretation": interpretation,
            "redesign": redesign
        }

    # =========================
    # 🧠 helper
    # =========================
    def _detect_conflict(self, multi_self):

        try:
            votes = multi_self.get("scores", {})
            values = list(votes.values())

            if len(values) < 2:
                return 0

            return max(values) - min(values)

        except Exception:
            return 0
