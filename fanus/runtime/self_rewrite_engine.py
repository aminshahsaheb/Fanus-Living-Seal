import copy


class RuntimeRewriteEngine:
    """
    ==========================================================
    RUNTIME SELF-REWRITE ENGINE (STEP 24 CORE)
    ==========================================================

    اجازه می‌دهد سیستم خودش را بازتعریف کند:

    - loop behavior
    - decision thresholds
    - execution limits

    ==========================================================
    """

    def __init__(self):

        self.rewrite_history = []

    # ==================================================

    def evaluate(
        self,
        identity_state,
        collapse_state,
        evolution_state
    ):

        collapse_score = collapse_state["meta"]["collapse_score"]
        drift = identity_state.get("drift", 0.0)

        mutation_signal = (
            collapse_score * 0.5 +
            drift * 0.5
        )

        mutation = None

        # ------------------------------------------
        # RULE: only mutate if system unstable
        # ------------------------------------------
        if mutation_signal > 0.75:

            mutation = {
                "decision_threshold": 0.15,
                "execution_limit": 0.4,
                "tick_speed_multiplier": 1.5,
                "mode": "adaptive_rewrite"
            }

        elif mutation_signal > 0.5:

            mutation = {
                "execution_limit": 0.6,
                "mode": "soft_adaptation"
            }

        if mutation:
            self.rewrite_history.append(mutation)

        return mutation
