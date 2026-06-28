"""
==========================================================
FANUS DECISION ENGINE
==========================================================

Canonical Decision Engine

Responsibilities
----------------

Convert semantic events into executable runtime decisions.

This module NEVER:

- modifies identity
- modifies memory
- modifies evolution
- modifies collapse

It only decides the next runtime action.

==========================================================
"""


class DecisionEngine:

    """
    Runtime decision engine.
    """

    def evaluate(

        self,

        identity_state,

        evolution_state,

        collapse_state

    ):

        # ----------------------------------
        # Collapse Event
        # ----------------------------------

        collapse_event = collapse_state.get(

            "event",

            {}

        )

        collapse_payload = collapse_event.get(

            "payload",

            {}

        )

        # ----------------------------------
        # Critical collapse
        # ----------------------------------

        if collapse_payload.get(

            "recovery_mode",

            False

        ):

            return "ENTER_STABILIZATION_MODE"

        # ----------------------------------
        # Identity instability
        # ----------------------------------

        if identity_state.get(

            "stability",

            1.0

        ) < 0.20:

            return "ENTER_STABILIZATION_MODE"

        # ----------------------------------
        # Evolution proposal
        # ----------------------------------

        proposals = evolution_state.get(

            "proposals",

            []

        )

        if proposals:

            proposal = proposals[0]

            if isinstance(proposal, dict):

                payload = proposal.get(

                    "payload",

                    proposal

                )

                return payload.get(

                    "action",

                    "ALLOW_WITH_CAUTION"

                )

        # ----------------------------------
        # Default
        # ----------------------------------

        return "ALLOW_WITH_CAUTION"
