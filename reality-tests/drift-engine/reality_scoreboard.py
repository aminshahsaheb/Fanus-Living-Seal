from drift_engine import DriftEngine

class RealityScoreboard:

    def __init__(self):
        self.engine = DriftEngine()

    def evaluate_system(self, test_cases):

        scores = []

        for t in test_cases:
            result = self.engine.evaluate(
                t["system_output"],
                t["external"],
                t["truth"]
            )

            scores.append(result.total())

        avg = sum(scores) / len(scores)

        state = self._classify(avg)

        return {
            "average_drift": avg,
            "state": state,
            "raw_scores": scores
        }

    def _classify(self, score):

        if score < 0.25:
            return "STABLE"
        elif score < 0.5:
            return "FRAGILE"
        elif score < 0.75:
            return "DRIFTING"
        else:
            return "SELF-SEALING"
