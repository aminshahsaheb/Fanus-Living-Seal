from typing import Dict, List


class TrustEngine:

    def __init__(self):

        # ─────────────────────────────
        # CORE MEMORY
        # ─────────────────────────────
        self.trust_score = 1.0
        self.history: List[Dict] = []

        # ─────────────────────────────
        # LEARNING RATES
        # ─────────────────────────────
        self.alpha = 0.15  # decay
        self.beta = 0.25   # reward/punish strength

    # ─────────────────────────────
    # MAIN UPDATE FUNCTION
    # ─────────────────────────────
    def update(self, output: dict, state: dict, identity: dict) -> dict:

        drift = float(output.get("drift", 0.0))

        grounding = output.get("grounding", {})
        mismatch = grounding.get("mismatch", False)

        boundary = output.get("boundary", {})
        blocked = boundary.get("allowed", True) is False

        # ─────────────────────────────
        # 1. BASE PENALTY FROM DRIFT
        # ─────────────────────────────
        drift_penalty = drift * 0.4

        # ─────────────────────────────
        # 2. REALITY MISMATCH PENALTY
        # ─────────────────────────────
        mismatch_penalty = 0.3 if mismatch else 0.0

        # ─────────────────────────────
        # 3. BOUNDARY VIOLATION PENALTY
        # ─────────────────────────────
        boundary_penalty = 0.25 if blocked else 0.0

        # ─────────────────────────────
        # 4. IDENTITY STABILITY BONUS
        # ─────────────────────────────
        identity_stability = identity.get("stability", 0.5)
        identity_bonus = identity_stability * 0.2

        # ─────────────────────────────
        # 5. FINAL TRUST DELTA
        # ─────────────────────────────
        delta = (
            - drift_penalty
            - mismatch_penalty
            - boundary_penalty
            + identity_bonus
        )

        # ─────────────────────────────
        # 6. APPLY SMOOTH UPDATE
        # ─────────────────────────────
        self.trust_score = (
            (1 - self.alpha) * self.trust_score
            + self.beta * delta
        )

        # clamp
        self.trust_score = max(0.0, min(1.0, self.trust_score))

        # ─────────────────────────────
        # 7. STORE MEMORY
        # ─────────────────────────────
        self.history.append({
            "drift": drift,
            "mismatch": mismatch,
            "blocked": blocked,
            "trust": self.trust_score
        })

        # ─────────────────────────────
        # 8. RETURN STATE
        # ─────────────────────────────
        return {
            "trust_score": round(self.trust_score, 4),
            "trend": self._trend(),
            "risk_level": self._risk_level()
        }

    # ─────────────────────────────
    # TRUST TREND
    # ─────────────────────────────
    def _trend(self) -> str:

        if len(self.history) < 3:
            return "insufficient_data"

        recent = [h["trust"] for h in self.history[-3:]]

        if recent[-1] > recent[0]:
            return "increasing"
        elif recent[-1] < recent[0]:
            return "decreasing"
        else:
            return "stable"

    # ─────────────────────────────
    # RISK CLASSIFICATION
    # ─────────────────────────────
    def _risk_level(self) -> str:

        if self.trust_score > 0.75:
            return "low_risk"
        elif self.trust_score > 0.4:
            return "medium_risk"
        else:
            return "high_risk"
