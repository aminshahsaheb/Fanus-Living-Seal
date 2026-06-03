class DriftEngine:
    """
    DriftEngine v1

    Computes system-level drift based on:
    - Epistemic validity
    - Narrative distortion
    - Compression stability
    - Alignment integrity

    Output: drift score between 0 and 1 (higher = more drift)
    """

    def __init__(self,
                 w_epistemic=0.25,
                 w_narrative=0.25,
                 w_compression=0.10,
                 w_alignment=0.40):

        self.w_epistemic = w_epistemic
        self.w_narrative = w_narrative
        self.w_compression = w_compression
        self.w_alignment = w_alignment

    def compute(self, epistemic, narrative, compression, alignment):
        """
        Compute drift score.

        Parameters:
            epistemic (float): truth alignment (0..1)
            narrative (float): narrative distortion (0..1)
            compression (float): structural stability (0..1)
            alignment (float): relational alignment (0..1)

        Returns:
            float: drift score (0..1)
        """

        drift = (
            self.w_epistemic * epistemic +
            self.w_narrative * narrative +
            self.w_compression * compression +
            self.w_alignment * (1 - alignment)
        )

        return self._clamp(drift)

    def explain(self, epistemic, narrative, compression, alignment):
        """
        Returns breakdown of drift components (useful for debugging/tests)
        """

        components = {
            "epistemic": self.w_epistemic * epistemic,
            "narrative": self.w_narrative * narrative,
            "compression": self.w_compression * compression,
            "alignment": self.w_alignment * (1 - alignment),
        }

        components["drift_total"] = sum(components.values())

        return components

    def _clamp(self, value):
        """
        Keep drift in safe range [0, 1]
        """
        return max(0.0, min(1.0, value))
