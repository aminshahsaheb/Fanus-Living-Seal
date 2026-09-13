from collections import defaultdict


class MemoryTimeline:

    def __init__(self):

        # timeline اصلی (روایت زمانی)
        self.timeline = []

        # نگاشت علت → نتیجه
        self.causal_map = defaultdict(list)

    # =========================
    # 🧠 1. ADD EVENT
    # =========================
    def add_event(self, event, decision, identity_state):

        node = {
            "intent": event.get("intent"),
            "decision": decision,
            "identity": identity_state,
            "timestamp": len(self.timeline)
        }

        self.timeline.append(node)

        return node

    # =========================
    # 🧠 2. BUILD CAUSAL LINKS
    # =========================
    def build_causality(self):

        for i in range(1, len(self.timeline)):

            prev = self.timeline[i - 1]
            curr = self.timeline[i]

            key = f"{prev['decision']} → {curr['decision']}"

            self.causal_map[key].append({
                "from": prev,
                "to": curr
            })

        return dict(self.causal_map)

    # =========================
    # 🧠 3. DETECT PATTERNS OVER TIME
    # =========================
    def detect_drift(self):

        if len(self.timeline) < 3:
            return "stable"

        decisions = [t["decision"] for t in self.timeline[-5:]]

        if decisions.count("BLOCK") > 2:
            return "risk_drift"

        if decisions.count("ALLOW_CONFIDENT") > 3:
            return "expansion_drift"

        return "balanced"

    # =========================
    # 🧠 4. GENERATE STORY
    # =========================
    def generate_story(self):

        if not self.timeline:
            return "No history yet."

        last = self.timeline[-1]

        story = f"""
Fanus Timeline Summary:

Latest Intent: {last['intent']}
Latest Decision: {last['decision']}
Identity State: {last['identity']}

Evolution Size: {len(self.timeline)} events
"""

        drift = self.detect_drift()

        story += f"\nBehavior Drift: {drift}\n"

        return story

    # =========================
    # 🧠 5. FULL UPDATE PIPELINE
    # =========================
    def update(self, event, decision, identity_state):

        self.add_event(event, decision, identity_state)

        causality = self.build_causality()

        story = self.generate_story()

        return {
            "timeline_length": len(self.timeline),
            "causality": causality,
            "story": story
        }
