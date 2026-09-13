class SystemIdentity:
    """
    V5.34.0 — System Identity Layer

    هدف:
    تعریف هویت ثابت سیستم و جلوگیری از drift هویتی
    """

    def __init__(self):

        # ─────────────────────────────
        # CORE IDENTITY VECTOR
        # ─────────────────────────────
        self.identity_vector = {
            "purpose": "stability_through_observation",
            "nature": "bounded_adaptive_system",
            "behavior": "consistent_under_constraint"
        }

        # ─────────────────────────────
        # IDENTITY STABILITY SCORE
        # ─────────────────────────────
        self.identity_integrity = 1.0

    def evaluate(self, system_state: dict):

        # ─────────────────────────────
        # 1. PURPOSE ALIGNMENT CHECK
        # ─────────────────────────────
        purpose_match = system_state.get("purpose") == self.identity_vector["purpose"]

        # ─────────────────────────────
        # 2. BEHAVIOR ALIGNMENT CHECK
        # ─────────────────────────────
        behavior_match = system_state.get("behavior") == self.identity_vector["behavior"]

        # ─────────────────────────────
        # 3. NATURE CHECK
        # ─────────────────────────────
        nature_match = system_state.get("nature") == self.identity_vector["nature"]

        # ─────────────────────────────
        # 4. IDENTITY SCORE
        # ─────────────────────────────
        matches = sum([purpose_match, behavior_match, nature_match])

        self.identity_integrity = matches / 3

        # ─────────────────────────────
        # 5. IDENTITY DRIFT DETECTION
        # ─────────────────────────────
        if self.identity_integrity < 0.5:
            status = "IDENTITY_DRIFT_WARNING"

        elif self.identity_integrity < 0.8:
            status = "MINOR_DEVIATION"

        else:
            status = "STABLE_IDENTITY"

        # ─────────────────────────────
        # 6. OUTPUT
        # ─────────────────────────────
        return {
            "identity_integrity": self.identity_integrity,
            "status": status,
            "identity_vector": self.identity_vector
        }
