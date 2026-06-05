class DriftEngine:
    def compute(self, epistemic, narrative, compression, alignment):
        drift = (
            0.30 * epistemic +
            0.20 * narrative +
            0.10 * compression +
            0.40 * (1 - alignment)
        )
        return float(drift)
