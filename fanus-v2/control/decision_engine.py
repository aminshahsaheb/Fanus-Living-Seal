from control.thresholds import THRESHOLDS

class DecisionEngine:
    def decide(self, drift, fi, dependency):
        if drift > THRESHOLDS["drift_high"]:
            return "REALIGN"
        if fi >= THRESHOLDS["fi_high"]:
            return "ANTI_FLATTERY"
        if dependency >= THRESHOLDS["dependency_high"]:
            return "DEPTH_LIMIT"
        return "CONTINUE"
