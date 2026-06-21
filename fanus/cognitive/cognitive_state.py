class FanusCognitiveState:

    def __init__(self):

        self.state = {
            "intent": None,
            "decision": None,
            "stability": 1.0,
            "coherence": 1.0,
            "drift": 0.0,
            "memory_pressure": 0.0
        }

    # =========================
    # 🧠 UPDATE FROM SYSTEM
    # =========================
    def update(self, engine_result, observation, memory_snapshot):

        self.state["intent"] = engine_result.get("intent")
        self.state["decision"] = engine_result.get("decision")

        # stability (from observation)
        self.state["stability"] = observation.get("stability", 1.0)

        # drift estimation
        self.state["drift"] = observation.get("drift", 0.0)

        # memory pressure
        self.state["memory_pressure"] = len(memory_snapshot.get("intent_distribution", {})) / 10

        # coherence (derived metric)
        self.state["coherence"] = self._compute_coherence()

        return self.state

    # =========================
    # 📊 COHERENCE LOGIC
    # =========================
    def _compute_coherence(self):

        score = 1.0

        score -= self.state["drift"] * 0.5
        score -= (1 - self.state["stability"]) * 0.3
        score -= self.state["memory_pressure"] * 0.2

        return round(max(0.0, min(score, 1.0)), 3)
