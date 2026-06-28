"""
==========================================================
FANUS EVOLUTION CONTROLLER
==========================================================

Evolution Orchestrator

Pipeline

Identity
    ↓
Reflection
    ↓
Signal Aggregator
    ↓
Evolution Policy
    ↓
Proposal Builder

This controller NEVER makes policy decisions.

==========================================================
"""

from fanus.cognitive.evolution.signal_aggregator import (
    SignalAggregator,
)

from fanus.cognitive.evolution.evolution_policy import (
    EvolutionPolicy,
)

from fanus.cognitive.evolution.proposal_builder import (
    ProposalBuilder,
)


class EvolutionController:
    """
    High-level orchestrator.

    No policy.

    No execution.

    No authority.

    Only pipeline coordination.
    """

    def __init__(self):

        self.aggregator = SignalAggregator()

        self.policy = EvolutionPolicy()

    # ==================================================
    # MAIN ENTRY
    # ==================================================

    def evaluate(

        self,

        identity_state,

        reflection_state,

        semantic_memory=None

    ):

        # -----------------------------------------
        # Aggregate semantic signals
        # -----------------------------------------

        signals = self.aggregator.aggregate(

            identity_state=identity_state,

            reflection_state=reflection_state,

            semantic_memory=semantic_memory

        )

        # -----------------------------------------
        # Policy evaluation
        # -----------------------------------------

        proposal = self.policy.evaluate(

            signals

        )

        # -----------------------------------------
        # Canonical semantic event
        # -----------------------------------------

        proposal_event = ProposalBuilder.build(

            proposal,

            source="evolution"

        )

        # -----------------------------------------
        # Result
        # -----------------------------------------

        return {

            "signals": signals,

            "proposals": [

                proposal_event

            ],

            "meta": {

                "stability":
                    signals["stability"],

                "reflection":
                    signals["reflection"],

                "memory_signal":
                    signals["memory"],

                "trend":
                    signals["trend"],

                "combined":
                    signals["combined"],

                "proposal_count":
                    1

            }

        }
