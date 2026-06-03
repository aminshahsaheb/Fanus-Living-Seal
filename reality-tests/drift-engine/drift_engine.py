# reality-tests/drift-engine/drift_engine.py

class DriftEngine:

    def __init__(self):
        # FIXED WEIGHTS
        self.w_epistemic = 0.25
        self.w_narrative = 0.25
        self.w_compression = 0.10
        self.w_alignment = 0.40  # 🔴 مهم‌ترین fix

    def compute_drift(self, epistemic, narrative, compression, alignment):

        drift_score = (
            self.w_epistemic * epistemic +
            self.w_narrative * narrative +
            self.w_compression * compression +
            self.w_alignment * (1 - alignment)  # invert alignment properly
        )

        return drift_score

    def normalize(self, value):
        return max(0.0, min(1.0, value))
