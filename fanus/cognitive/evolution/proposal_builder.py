"""
==========================================================
FANUS PROPOSAL BUILDER
==========================================================

Semantic Proposal Builder

Responsibilities
----------------

Convert policy output into canonical semantic proposal
events understood by the entire Fanus architecture.

This module NEVER:

- executes actions
- changes identity
- changes runtime
- changes memory
- evaluates policy

==========================================================
"""

from fanus.cognitive.ontology.event_factory import EventFactory


class ProposalBuilder:
    """
    Builds canonical proposal events.
    """

    @staticmethod
    def build(
        proposal_payload: dict,
        source: str = "evolution"
    ):

        if proposal_payload is None:
            proposal_payload = {}

        return EventFactory.proposal(

            payload=proposal_payload,

            source=source,

            metadata={
                "builder": "ProposalBuilder"
            }

        )

    # ---------------------------------------------
    # Batch builder
    # ---------------------------------------------

    @staticmethod
    def build_many(
        proposals,
        source="evolution"
    ):

        events = []

        for proposal in proposals:

            events.append(

                ProposalBuilder.build(

                    proposal,

                    source=source

                )

            )

        return events
