"""
==========================================================
FANUS COLLAPSE CONTROLLER
==========================================================

Collapse Orchestrator

Pipeline

Identity
    ↓
Reflection
    ↓
Evolution
    ↓
Collapse Analyzer
    ↓
Collapse Policy
    ↓
Collapse Event Builder

This controller NEVER:

- freezes runtime
- edits identity
- changes evolution

It only orchestrates collapse evaluation.

==========================================================
"""

from fanus.cognitive.collapse.collapse_analyzer import (
    CollapseAnalyzer,
)

from fanus.cognitive.collapse.collapse_policy import (
    CollapsePolicy,
)

from fanus.cognitive.collapse.collapse_event_builder import (
    CollapseEventBuilder,
)


class CollapseController:

    def __init__(self):

        self.analyzer = CollapseAnalyzer()

        self.policy = CollapsePolicy()

    # --------------------------------------------------

    def evaluate(

        self,

        identity_state,

        evolution_state,

        reflection_state=None

    ):

        # -------------------------
        # Aggregate signals
        # -------------------------

        signals = self.analyzer.aggregate(

            identity_state=identity_state,

            evolution_state=evolution_state,

            reflection_state=reflection_state

        )

        # -------------------------
        # Evaluate policy
        # -------------------------

        collapse = self.policy.evaluate(

            signals

        )

        # -------------------------
        # Canonical Event
        # -------------------------

        collapse_event = CollapseEventBuilder.build(

            collapse,

            source="collapse"

        )

        return {

            "signals": signals,

            "event": collapse_event,

            "meta": {

                "collapse_score":

                    collapse["collapse_score"],

                "alert_level":

                    collapse["alert_level"],

                "recovery_mode":

                    collapse["recovery_mode"]

            }

        }
