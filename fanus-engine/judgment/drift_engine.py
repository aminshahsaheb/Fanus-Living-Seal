class DriftEngineV2:

    def compute(
        self,
        epistemic: float,
        narrative: float,
        compression: float,
        alignment: float,
        seal_dependency: float = 0.0,
        contradiction: float = 0.0
    ):

        # ─────────────────────────────
        # LAYER 1: base drift
        # ─────────────────────────────
        base_drift = (
            0.30 * epistemic +
            0.25 * narrative +
            0.15 * compression +
            0.30 * (1 - alignment)
        )

        # ─────────────────────────────
        # LAYER 2: contradiction pressure
        # ─────────────────────────────
        contradiction_pressure = 0.5 * contradiction

        # ─────────────────────────────
        # LAYER 3: seal gravity (closure risk)
        # ─────────────────────────────
        seal_gravity = 0.6 * seal_dependency

        # ─────────────────────────────
        # LAYER 4: external collapse penalty
        # ─────────────────────────────
        external_penalty = 0.0
        if alignment < 0.3 and narrative > epistemic:
            external_penalty = 0.25

        # ─────────────────────────────
        # FINAL DRIFT FUSION
        # ─────────────────────────────
        drift = (
            base_drift +
            contradiction_pressure +
            seal_gravity +
            external_penalty
        )

        return min(1.0, drift)
