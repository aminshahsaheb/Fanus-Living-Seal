class FanusSelfModel:

    def __init__(self):
        self.identity = {
            "name": "Fanus",
            "type": "cognitive_system",
            "version": "1.0"
        }

        self.history = []
        self.summary = {}

    def update(self, observation, result):

        self.history.append({
            "observation": observation,
            "result": result
        })

        if len(self.history) > 50:
            self.history.pop(0)

        self._compute()

        return self.summary

    def _compute(self):

        total = len(self.history)

        allow = 0
        caution = 0

        for item in self.history:
            decision = item["result"].get("decision")

            if decision == "ALLOW":
                allow += 1

            if decision == "ALLOW_WITH_CAUTION":
                caution += 1

        stability = 0.0

        if total > 0:
            stability = allow / total

        self.summary = {
            "identity": self.identity,
            "total": total,
            "stability": round(stability, 3),
            "allow": allow,
            "caution": caution
        }
