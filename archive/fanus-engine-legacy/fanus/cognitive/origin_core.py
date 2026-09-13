class OriginCore:

    def __init__(self):

        self.purpose_history = []
        self.stable_meaning = None

    # =========================
    # 🧠 1. INFER PURPOSE
    # =========================
    def infer_purpose(self, system_state, meta_self):

        signals = []

        signals.append(system_state.get("goal_alignment", 0))
        signals.append(system_state.get("stability", 0))
        signals.append(meta_self.get("analysis", {}).get("identity_stability", 0))

        avg_signal = sum(signals) / len(signals)

        if avg_signal > 0.7:
            return "stabilize_and_preserve_intelligence"

        elif avg_signal > 0.4:
            return "optimize_under_constraints"

        else:
            return "recover_and_restructure"

    # =========================
    # 🧠 2. EMERGE VALUE SYSTEM
    # =========================
    def emerge_values(self, history):

        values = {
            "coherence": 0,
            "adaptability": 0,
            "stability": 0
        }

        for h in history[-20:]:

            if h.get("decision") == "ALLOW":
                values["coherence"] += 1

            if h.get("decision") == "ALLOW_WITH_CAUTION":
                values["adaptability"] += 1

            if h.get("decision") == "BLOCK":
                values["stability"] += 1

        total = sum(values.values()) or 1

        return {
            k: v / total for k, v in values.items()
        }

    # =========================
    # 🧠 3. COMPRESS MEANING
    # =========================
    def compress_meaning(self, purpose, values):

        return {
            "core_purpose": purpose,
            "dominant_value": max(values, key=values.get),
            "value_vector": values
        }

    # =========================
    # 🧠 4. GENERATE DIRECTION
    # =========================
    def generate_direction(self, meaning):

        if meaning["core_purpose"] == "stabilize_and_preserve_intelligence":
            return "preserve_current_architecture"

        if meaning["core_purpose"] == "optimize_under_constraints":
            return "gradual_self_improvement"

        return "emergency_restructuring_mode"

    # =========================
    # 🧠 5. ALIGN SYSTEM
    # =========================
    def align(self, direction, system_state):

        system_state["direction"] = direction
        return system_state

    # =========================
    # 🧠 FULL PIPELINE
    # =========================
    def run(self, system_state, meta_self, history):

        purpose = self.infer_purpose(system_state, meta_self)

        values = self.emerge_values(history)

        meaning = self.compress_meaning(purpose, values)

        direction = self.generate_direction(meaning)

        aligned_state = self.align(direction, system_state)

        return {
            "purpose": purpose,
            "values": values,
            "meaning": meaning,
            "direction": direction,
            "aligned_state": aligned_state
        }
