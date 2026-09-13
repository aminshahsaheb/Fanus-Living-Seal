import time


class ConsciousnessLoop:

    def __init__(self):

        # روایت ذهنی سیستم (memory of thinking)
        self.thought_history = []

    # =========================
    # 🧠 1. OBSERVE DECISION
    # =========================
    def observe(self, event, decision, internal_state):

        snapshot = {
            "timestamp": time.time(),
            "intent": event.get("intent"),
            "decision": decision,
            "state": internal_state
        }

        self.thought_history.append(snapshot)

        return snapshot

    # =========================
    # 🧠 2. BUILD SELF-NARRATIVE
    # =========================
    def build_narrative(self):

        if len(self.thought_history) < 2:
            return "I am beginning to observe my decisions."

        last = self.thought_history[-1]
        prev = self.thought_history[-2]

        if last["decision"] != prev["decision"]:
            return "I changed my mind after observing myself."

        return "My decisions follow a stable pattern."

    # =========================
    # 🧠 3. DETECT SELF-CONTRADICTION
    # =========================
    def detect_contradiction(self):

        contradictions = 0

        for i in range(1, len(self.thought_history)):

            if self.thought_history[i]["decision"] != self.thought_history[i-1]["decision"]:
                contradictions += 1

        return contradictions

    # =========================
    # 🧠 4. REFLECTIVE STATE
    # =========================
    def reflect(self):

        contradictions = self.detect_contradiction()

        if contradictions > 3:
            return "unstable_identity"

        if contradictions == 0:
            return "rigid_identity"

        return "adaptive_identity"

    # =========================
    # 🧠 5. FULL LOOP OUTPUT
    # =========================
    def run(self, event, decision, internal_state):

        observation = self.observe(event, decision, internal_state)

        narrative = self.build_narrative()

        state = self.reflect()

        return {
            "observation": observation,
            "narrative": narrative,
            "conscious_state": state,
            "contradictions": self.detect_contradiction()
        }
