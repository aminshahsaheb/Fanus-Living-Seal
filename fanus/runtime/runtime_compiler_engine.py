class RuntimeCompilerEngine:
    """
    ==========================================================
    RUNTIME COMPILER ENGINE (STEP 25 FINAL CORE)
    ==========================================================

    Converts system instability into runtime recompilation.

    This is NOT execution logic.

    This is structural system evolution logic.
    ==========================================================
    """

    def __init__(self):

        self.compile_history = []

    # ==================================================

    def evaluate(
        self,
        identity_state,
        evolution_state,
        collapse_state,
        runtime_config
    ):

        collapse_score = collapse_state["meta"]["collapse_score"]
        stability = identity_state.get("stability", 1.0)
        trend = evolution_state["signals"]["trend"]

        # ------------------------------------------
        # compilation pressure
        # ------------------------------------------
        pressure = (
            collapse_score * 0.5 +
            (1.0 - stability) * 0.3 +
            abs(trend) * 0.2
        )

        compiled = None

        # ------------------------------------------
        # DEEP RECOMPILATION
        # ------------------------------------------
        if pressure > 0.8:

            compiled = {
                "execution_limit": 0.25,
                "decision_threshold": 0.1,
                "tick_speed_multiplier": 1.8,
                "mode": "deep_compilation"
            }

        # ------------------------------------------
        # ADAPTIVE COMPILATION
        # ------------------------------------------
        elif pressure > 0.55:

            compiled = {
                "execution_limit": 0.5,
                "tick_speed_multiplier": 1.3,
                "mode": "adaptive_compilation"
            }

        # ------------------------------------------
        # LIGHT TUNING
        # ------------------------------------------
        elif pressure > 0.35:

            compiled = {
                "tick_speed_multiplier": 1.1,
                "mode": "light_tuning"
            }

        if compiled:
            self.compile_history.append(compiled)

        return compiled
