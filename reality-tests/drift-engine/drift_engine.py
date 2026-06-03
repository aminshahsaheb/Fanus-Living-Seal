"""
Drift Engine (Fanus Reality Layer)

Purpose:
Compute epistemic drift across 4 dimensions:

- Epistemic coherence (truth alignment)
- Narrative closure (story self-consistency bias)
- Compression (over-simplification of reality)
- Alignment (internal vs external consistency)

Final Drift Score = weighted aggregate
"""

from dataclasses import dataclass


@dataclass
class DriftComponents:
    epistemic: float
    narrative: float
    compression: float
    alignment: float


class DriftEngine:

    def __init__(self):
        # weights tuned to fix your current ~0.59 drift inflation
        self.w_epistemic = 0.35
        self.w_narrative = 0.20
        self.w_compression = 0.20
        self.w_alignment = 0.25

    def compute(self, c: DriftComponents) -> float:
        """
        Lower = better coherence, higher = drift risk
        """

        drift = (
            (1 - c.epistemic) * self.w_epistemic +
            c.narrative * self.w_narrative +
            c.compression * self.w_compression +
            (1 - c.alignment) * self.w_alignment
        )

        return round(drift, 6)

    def explain(self, c: DriftComponents) -> dict:
        return {
            "drift": self.compute(c),
            "epistemic_risk": 1 - c.epistemic,
            "narrative_pressure": c.narrative,
            "compression_loss": c.compression,
            "alignment_gap": 1 - c.alignment
        }
