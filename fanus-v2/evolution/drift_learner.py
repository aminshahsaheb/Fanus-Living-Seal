import statistics

class DriftLearner:
    def __init__(self, ledger):
        self.ledger = ledger

    def get_drift_trend(self, n_last=5):
        entries = self.ledger.get_last_n(n_last)
        if len(entries) < 2:
            return None
        drifts = [e["drift"] for e in entries if "drift" in e]
        if len(drifts) < 2:
            return None
        avg = statistics.mean(drifts)
        trend = "stable"
        if drifts[-1] > avg * 1.1:
            trend = "increasing"
        elif drifts[-1] < avg * 0.9:
            trend = "decreasing"
        return {"avg": round(avg, 3), "trend": trend, "last": drifts[-1]}

    def suggest_new_thresholds(self):
        trend_data = self.get_drift_trend()
        if not trend_data:
            return None
        new_thresholds = {}
        if trend_data["trend"] == "increasing":
            new_thresholds["drift_high"] = max(0.55, trend_data["avg"] + 0.05)
        elif trend_data["trend"] == "decreasing":
            new_thresholds["drift_high"] = min(0.75, trend_data["avg"] - 0.05)
        else:
            new_thresholds["drift_high"] = 0.65  # default
        return new_thresholds
