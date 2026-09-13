import random


class MultiSelfDialogue:

    def __init__(self):

        # سه "خود" داخلی
        self.selves = {
            "guardian": 1.2,
            "explorer": 1.0,
            "analyst": 1.1
        }

    # =========================
    # 🧠 1. GENERATE INTERNAL VIEWS
    # =========================
    def generate_views(self, event, history):

        intent = event.get("intent", "unknown")

        views = {}

        # GUARDIAN: محافظه‌کار
        views["guardian"] = {
            "decision": "BLOCK" if len(history) > 5 else "ALLOW_WITH_CAUTION",
            "reason": "risk control priority"
        }

        # EXPLORER: ریسک‌پذیر
        views["explorer"] = {
            "decision": "ALLOW_CONFIDENT",
            "reason": "maximize exploration"
        }

        # ANALYST: منطقی
        success = sum(1 for h in history if h.get("decision") == "ALLOW")
        views["analyst"] = {
            "decision": "ALLOW_CONFIDENT" if success > 3 else "ALLOW",
            "reason": "pattern-based evaluation"
        }

        return views

    # =========================
    # 🧠 2. DEBATE ENGINE
    # =========================
    def debate(self, views):

        arguments = []

        for name, view in views.items():
            arguments.append({
                "self": name,
                "decision": view["decision"],
                "reason": view["reason"]
            })

        return arguments

    # =========================
    # 🧠 3. WEIGHTED VOTING
    # =========================
    def vote(self, debate_results):

        scores = {
            "ALLOW": 0.0,
            "ALLOW_WITH_CAUTION": 0.0,
            "ALLOW_CONFIDENT": 0.0,
            "BLOCK": 0.0
        }

        for d in debate_results:

            weight = self.selves[d["self"]]

            scores[d["decision"]] += weight

        final = max(scores.items(), key=lambda x: x[1])[0]

        return final, scores

    # =========================
    # 🧠 4. FULL DIALOGUE PIPELINE
    # =========================
    def run(self, event, history):

        views = self.generate_views(event, history)

        debate_results = self.debate(views)

        final_decision, scores = self.vote(debate_results)

        return {
            "views": views,
            "debate": debate_results,
            "scores": scores,
            "final_decision": final_decision
        }
