"""
==========================================================
FANUS COLLAPSE EVENT BUILDER
==========================================================

Canonical builder for semantic collapse events.

Responsibilities
----------------

Convert collapse assessment into a canonical semantic
event using EventFactory.

This module NEVER:

- evaluates collapse
- changes runtime
- freezes the system

==========================================================
"""

from fanus.cognitive.ontology.event_factory import EventFactory


class CollapseEventBuilder:

    @staticmethod
    def build(

        collapse_result,

        source="collapse",

        metadata=None

    ):

        return EventFactory.collapse(

            payload=collapse_result,

            source=source,

            metadata=metadata

        )
