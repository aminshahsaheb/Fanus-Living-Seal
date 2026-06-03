class ThresholdPolicy:

    def __init__(self):
        self.low = 0.3
        self.medium = 0.6
        self.high = 0.8

    def evaluate(self, drift_score: float):

        if drift_score < self.low:
            return "stable"

        elif drift_score < self.medium:
            return "watch"

        elif drift_score < self.high:
            return "realign"

        else:
            return "critical"
