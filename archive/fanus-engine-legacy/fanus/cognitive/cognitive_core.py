import random
from collections import defaultdict


class CognitiveCore:

    def __init__(self):

        # internal motivation map
        self.goal_space = [
            "stability",
            "exploration",
            "compression",
            "self_improvement",
            "safety"
        ]

        self.state_memory = defaultdict(float)

    # =========================
    # 🧠 1. ANALYZE SYSTEM STATE
    # =========================
    def analyze_state(self, history):

        stats = {
            "success": 0,
            "fail": 0,
            "uncertain": 0
        }

        for h in history:
            d = h.get("decision")

            if d in ["ALLOW", "ALLOW_CONFIDENT"]:
                stats["success"] += 1
            elif d == "BLOCK":
                stats["fail"] += 1
            else:
                stats["uncertain"] += 1

        total = max(1, len(history))

        return {
            "success_rate": stats["success"] / total,
            "fail_rate": stats["fail"] / total,
            "uncertainty": stats["uncertain"] / total
        }

    # =========================
    # 🧠 2. GENERATE GOAL (core autonomy)
    # =========================
    def generate_goal(self, state):

        # rule-based emergence (first version of "autonomy")
        if state["fail_rate"] > 0.4:
            goal = "safety"

        elif state["success_rate"] > 0.7:
            goal = "exploration"

        elif state["uncertainty"] > 0.3:
            goal = "stability"

        else:
            goal = random.choice(self.goal_space)

        return goal

    # =========================
    # 🧠 3. UPDATE INTERNAL DRIVE
    # =========================
    def update_drive(self, goal):

        self.state_memory[goal] += 1.0

        # decay others
        for g in self.goal_space:
            if g != goal:
                self.state_memory[g] *= 0.95

    # =========================
    # 🧠 4. GET ACTIVE PRIORITY
    # =========================
    def get_priority(self):

        if not self.state_memory:
            return "stability"

        return max(self.state_memory.items(), key=lambda x: x[1])[0]
