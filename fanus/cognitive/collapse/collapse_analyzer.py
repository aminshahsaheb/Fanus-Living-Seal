"""
==========================================================
FANUS COLLAPSE ANALYZER
==========================================================

Semantic Collapse Analyzer

Responsibilities
----------------

Collect semantic signals required for collapse analysis.

This module NEVER:

- freezes the system
- makes decisions
- creates events
- changes runtime
- changes identity

It only aggregates semantic evidence.

==========================================================
"""


class CollapseAnalyzer:
    """
    Collapse signal aggregation layer.
    """

    def aggregate(

        self,

        identity_state,

        evolution_state,

        reflection_state=None

    ):

        stability = identity_state.get(

            "stability",

            1.0

        )

        mode = identity_state.get(

            "mode",

            "stable_core_state"

        )

        proposals = evolution_state.get(

            "proposals",

            []

        )

        proposal_count = len(proposals)

        reflection_signal = 1.0

        if reflection_state:

            reflection_signal = reflection_state.get(

                "signal_strength",

                1.0

            )

        return {

            "stability": stability,

            "mode": mode,

            "proposal_count": proposal_count,

            "reflection": reflection_signal

        }
