class TrustEngine:
    """
    V5.33 — Trust Without Freedom Engine

    هدف:
    ساخت اعتماد پایدار بدون نیاز به افزایش autonomy
    """

    def __init__(self):

        # ─────────────────────────────
        # TRUST STATE
        # ─────────────────────────────
        self.trust_score = 1.0

        # ─────────────────────────────
        # BEHAVIOR CONSISTENCY MEMORY
        # ─────────────────────────────
        self.history = []

        # ─────────────────────────────
        # STABILITY WEIGHT
        # ─────────────────────────────
        self.stability_weight = 0.7
        self.adaptability_weight = 0.3

    def update(self, output, expected_behavior):

        # ─────────────────────────────
        # 1. CONSISTENCY CHECK
        # ─────────────────────────────
        consistent = output == expected_behavior

        self.history.append(consistent)

        if len(self.history) > 20:
            self.history.pop(0)

        # ─────────────────────────────
        # 2. TRUST CALCULATION
        # ─────────────────────────────
        consistency_rate = sum(self.history) / len(self.history)

        self.trust_score = (
            self.stability_weight * consistency_rate +
            self.adaptability_weight * (1 - abs(0.5 - consistency_rate))
        )

        # ─────────────────────────────
        # 3. ADAPTIVE STABILIZATION (NOT FREEDOM)
        # ─────────────────────────────
        if self.trust_score < 0.5:
            action = "TIGHTEN_CONSTRAINTS"

        elif self.trust_score < 0.75:
            action = "STABILIZE_BEHAVIOR"

        else:
            action = "MAINTAIN_STATE"

        # ─────────────────────────────
        # 4. OUTPUT
        # ─────────────────────────────
        return {
            "trust_score": self.trust_score,
            "action": action,
            "consistency": consistency_rate
        }
