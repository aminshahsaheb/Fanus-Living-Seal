# fanus-engine/control/threshold_policy.py

class ThresholdPolicy:

    def __init__(self):
        self.watch = 0.3
        self.realign = 0.6
        self.critical = 0.8

    def evaluate(self, drift_score: float):

        if drift_score < self.watch:
            return "STABLE"

        elif drift_score < self.realign:
            return "WATCH"

        elif drift_score < self.critical:
            return "HIGH"

        else:
            return "CRITICAL"
