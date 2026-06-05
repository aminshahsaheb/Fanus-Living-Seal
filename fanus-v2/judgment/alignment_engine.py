class AlignmentEngine:
    def compute(self, external_signal: float, internal_signal: float) -> float:
        if external_signal == 0:
            return 0.0
        return min(internal_signal / external_signal, 1.0)
