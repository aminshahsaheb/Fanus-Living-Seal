from collections import defaultdict


class SymbolicIdentity:

    def __init__(self):

        # روایت داخلی سیستم
        self.identity_state = {
            "self_view": "undefined",
            "stability": 0.5,
            "conflicts": 0
        }

        self.pattern_memory = defaultdict(int)

    # =========================
    # 🧠 1. EXTRACT PATTERNS
    # =========================
    def extract_patterns(self, history):

        for h in history:
            d = h.get("decision")

            self.pattern_memory[d] += 1

        return dict(self.pattern_memory)

    # =========================
    # 🧠 2. BUILD SELF NARRATIVE
    # =========================
    def build_identity(self, patterns):

        total = sum(patterns.values()) or 1

        allow_ratio = patterns.get("ALLOW", 0) / total
        block_ratio = patterns.get("BLOCK", 0) / total

        if block_ratio > 0.4:
            self_view = "guardian"

        elif allow_ratio > 0.7:
            self_view = "explorer"

        else:
            self_view = "balanced_observer"

        self.identity_state["self_view"] = self_view

        return self_view

    # =========================
    # 🧠 3. CONTRADICTION CHECK
    # =========================
    def detect_conflict(self, history):

        conflicts = 0

        for i in range(1, len(history)):
            if history[i]["decision"] != history[i-1]["decision"]:
                conflicts += 1

        self.identity_state["conflicts"] = conflicts

        return conflicts

    # =========================
    # 🧠 4. STABILITY SCORE
    # =========================
    def compute_stability(self, patterns, conflicts):

        total = sum(patterns.values()) or 1

        stability = 1.0 - (conflicts / total)

        self.identity_state["stability"] = max(0.0, min(1.0, stability))

        return self.identity_state["stability"]

    # =========================
    # 🧠 5. GET IDENTITY IMPACT
    # =========================
    def get_behavior_modifier(self):

        if self.identity_state["self_view"] == "guardian":
            return {"risk_bias": -0.2}

        if self.identity_state["self_view"] == "explorer":
            return {"risk_bias": +0.2}

        return {"risk_bias": 0.0}
