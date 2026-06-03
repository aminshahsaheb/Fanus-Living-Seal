from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DriftResult:
    epistemic_drift: float
    narrative_drift: float
    compression_loss: float
    external_alignment: float

    def total(self):
        return (
            self.epistemic_drift +
            self.narrative_drift +
            self.compression_loss +
            (1 - self.external_alignment)
        ) / 4


class DriftEngine:

    def __init__(self):
        self.history: List[Dict] = []

    def evaluate(self, system_output: str, external_interpretation: str, ground_truth: str):

        epistemic_drift = self._simple_diff(system_output, ground_truth)
        narrative_drift = self._detect_self_reference(system_output)
        compression_loss = self._compression_stability(system_output, external_interpretation)
        external_alignment = self._alignment(system_output, external_interpretation)

        result = DriftResult(
            epistemic_drift,
            narrative_drift,
            compression_loss,
            external_alignment
        )

        self.history.append({
            "input": system_output,
            "external": external_interpretation,
            "truth": ground_truth,
            "score": result.total()
        })

        return result

    def _simple_diff(self, a, b):
        return 1 - min(len(set(a.split()) & set(b.split())) / max(len(set(b.split())), 1), 1)

    def _detect_self_reference(self, text):
        keywords = ["Witness", "Seal", "Novāyin", "Fānus"]
        hits = sum(1 for k in keywords if k in text)
        return min(hits / 5, 1)

    def _compression_stability(self, full, compressed):
        return 1 - abs(len(full) - len(compressed)) / max(len(full), 1)

    def _alignment(self, internal, external):
        return min(len(set(internal.split()) & set(external.split())) / max(len(external.split()), 1), 1)
