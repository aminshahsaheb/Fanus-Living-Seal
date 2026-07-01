"""
==========================================================
FANUS SELF STABILIZATION ENGINE
==========================================================

Adaptive control system for runtime stability.

This module:
- predicts collapse risk
- adjusts tick speed
- controls execution pressure
- stabilizes system dynamics

NEVER modifies identity or memory.
ONLY regulates runtime behavior.
==========================================================
"""


class SelfStabilizationEngine:

    def __init__(self):

        self.history = []
        self.base_tick = 0.2

    # -----------------------------------------
    # MAIN ENTRY
    # -----------------------------------------

    def evaluate(self, collapse_state, evolution_state):

        collapse_score = self._extract_collapse(collapse_state)

        stability = self._extract_stability(evolution_state)

        # -------------------------------------
        # adaptive logic
        # -------------------------------------

        tick_delay = self._compute_tick_delay(
            collapse_score,
            stability
        )

        execution_limit = self._compute_execution_limit(
            collapse_score
        )

        damping = self._compute_damping(
            collapse_score,
            stability
        )

        result = {

            "tick_delay": tick_delay,

            "execution_limit": execution_limit,

            "damping_factor": damping,

            "collapse_score": collapse_score,

            "stability": stability,

            "mode": self._mode(collapse_score)

        }

        self.history.append(result)

        return result

    # -----------------------------------------
    # collapse extraction
    # -----------------------------------------

    def _extract_collapse(self, collapse_state):

        try:
            return collapse_state["meta"]["collapse_score"]
        except:
            return 0.0

    # -----------------------------------------
    # stability extraction
    # -----------------------------------------

    def _extract_stability(self, evolution_state):

        try:
            return evolution_state["meta"]["stability"]
        except:
            return 1.0

    # -----------------------------------------
    # tick control
    # -----------------------------------------

    def _compute_tick_delay(self, collapse, stability):

        base = self.base_tick

        risk = collapse * 0.8

        return round(base + risk - stability * 0.05, 3)

    # -----------------------------------------
    # execution control
    # -----------------------------------------

    def _compute_execution_limit(self, collapse):

        if collapse > 0.7:
            return 1

        if collapse > 0.4:
            return 2

        return 5

    # -----------------------------------------
    # damping control
    # -----------------------------------------

    def _compute_damping(self, collapse, stability):

        return round(max(0.1, 1.0 - collapse + stability * 0.2), 3)

    # -----------------------------------------
    # system mode
    # -----------------------------------------

    def _mode(self, collapse):

        if collapse > 0.7:
            return "SAFE_MODE"

        if collapse > 0.4:
            return "STABILIZING"

        return "NORMAL"
