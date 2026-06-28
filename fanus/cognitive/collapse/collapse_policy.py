"""
==========================================================
FANUS COLLAPSE POLICY
==========================================================

Semantic Collapse Policy

Responsibilities
----------------

Evaluate semantic collapse risk from aggregated signals.

This module NEVER:

- creates events
- freezes runtime
- changes identity
- executes recovery

It only computes semantic collapse assessment.

==========================================================
"""


class CollapsePolicy:

    """
    Semantic collapse policy.
    """

    def evaluate(self, signals: dict):

        stability = signals.get("stability", 1.0)

        proposal_count = signals.get("proposal_count", 0)

        reflection = signals.get("reflection", 1.0)

        mode = signals.get("mode", "stable_core_state")

        collapse_score = 0.0

        # ----------------------------------
        # Identity instability
        # ----------------------------------

        collapse_score += (1.0 - stability) * 0.40

        # ----------------------------------
        # Reflection degradation
        # ----------------------------------

        collapse_score += (1.0 - reflection) * 0.30

        # ----------------------------------
        # Evolution pressure
        # ----------------------------------

        if proposal_count > 2:

            collapse_score += 0.20

        # ----------------------------------
        # Recovery / unstable modes
        # ----------------------------------

        if mode != "stable_core_state":

            collapse_score += 0.10

        collapse_score = max(
            0.0,
            min(1.0, collapse_score)
        )

        # ----------------------------------
        # Alert level
        # ----------------------------------

        if collapse_score < 0.30:

            alert = "LOW"

        elif collapse_score < 0.60:

            alert = "MEDIUM"

        else:

            alert = "HIGH"

        return {

            "collapse_score": round(collapse_score, 3),

            "alert_level": alert,

            "recovery_mode": collapse_score >= 0.80,

            "state": "MONITORING_ONLY"

        }
