# fanus-engine/learning/parameter_store.py

class ParameterStore:

    def __init__(self):
        self.weights = {
            "epistemic": 0.30,
            "narrative": 0.25,
            "compression": 0.15,
            "alignment": 0.30
        }

        self.thresholds = {
            "watch": 0.3,
            "high": 0.6,
            "critical": 0.8
        }

    def update_weight(self, key, value):
        self.weights[key] = max(0.0, min(1.0, value))

    def update_threshold(self, key, value):
        self.thresholds[key] = value
