class StabilityGovernor:
    """
    V5.29 — Stability Governor Layer

    هدف:
    جلوگیری از over-correction و نوسان سیستم
    """

    def __init__(self):

        # ─────────────────────────────
        # THRESHOLDS
        # ─────────────────────────────
        self.max_delta_per_cycle = 0.15
        self.max_consecutive_updates = 3
        self.instability_threshold = 0.65

        # history tracking
        self.update_history = []

    def evaluate(self, previous_params: dict, new_params: dict, drift: float):

        # ─────────────────────────────
        # 1. MEASURE CHANGE MAGNITUDE
        # ─────────────────────────────
        deltas = {}

        for k in new_params:
            old = previous_params.get(k, 0.0)
            new = new_params.get(k, 0.0)

            deltas[k] = abs(new - old)

        max_delta = max(deltas.values()) if deltas else 0.0

        # ─────────────────────────────
        # 2. DETECT INSTABILITY
        # ─────────────────────────────
        instability = drift > self.instability_threshold

        # ─────────────────────────────
        # 3. DETECT OVER-CORRECTION
        # ─────────────────────────────
        self.update_history.append(max_delta)

        if len(self.update_history) > 10:
            self.update_history.pop(0)

        recent_oscillation = sum(self.update_history) / len(self.update_history)

        over_correction = (
            max_delta > self.max_delta_per_cycle
            or recent_oscillation > self.max_delta_per_cycle
        )

        # ─────────────────────────────
        # 4. DECISION LOGIC
        # ─────────────────────────────
        if instability and over_correction:
            action = "LOCK_CALIBRATION"

        elif over_correction:
            action = "SLOW_DOWN"

        elif instability:
            action = "SOFT_RECALIBRATE"

        else:
            action = "STABLE"

        # ─────────────────────────────
        # 5. OUTPUT
        # ─────────────────────────────
        return {
            "action": action,
            "max_delta": max_delta,
            "instability": instability,
            "oscillation": recent_oscillation
        }
