"""
==========================================================
FANUS EVENT FACTORY
==========================================================

Single factory responsible for creating every semantic
event inside Fanus.

No runtime module should manually build events.

==========================================================
"""

from time import time

from fanus.cognitive.ontology.event_schema import (
    EVENT_ENTITIES,
    EVENT_TYPES,
)


class EventFactory:

    @staticmethod
    def _build(
        entity,
        semantic_type,
        payload,
        source="runtime",
        metadata=None
    ):

        if entity not in EVENT_ENTITIES:
            raise ValueError(f"Unknown entity: {entity}")

        if semantic_type not in EVENT_TYPES:
            raise ValueError(
                f"Unknown semantic type: {semantic_type}"
            )

        return {

            "entity": entity,

            "semantic_type": semantic_type,

            "timestamp": time(),

            "payload": payload,

            "source": source,

            "metadata": metadata or {}

        }

    # ----------------------------------------------------
    # Identity
    # ----------------------------------------------------

    @classmethod
    def identity(
        cls,
        payload,
        source="runtime",
        metadata=None
    ):

        return cls._build(

            entity="identity",

            semantic_type="state",

            payload=payload,

            source=source,

            metadata=metadata

        )

    # ----------------------------------------------------
    # Reflection
    # ----------------------------------------------------

    @classmethod
    def reflection(
        cls,
        payload,
        source="runtime",
        metadata=None
    ):

        return cls._build(

            entity="reflection",

            semantic_type="observation",

            payload=payload,

            source=source,

            metadata=metadata

        )

    # ----------------------------------------------------
    # Proposal
    # ----------------------------------------------------

    @classmethod
    def proposal(
        cls,
        payload,
        source="runtime",
        metadata=None
    ):

        return cls._build(

            entity="proposal",

            semantic_type="proposal",

            payload=payload,

            source=source,

            metadata=metadata

        )

    # ----------------------------------------------------
    # Decision
    # ----------------------------------------------------

    @classmethod
    def decision(
        cls,
        payload,
        source="runtime",
        metadata=None
    ):

        return cls._build(

            entity="decision",

            semantic_type="decision",

            payload=payload,

            source=source,

            metadata=metadata

        )

    # ----------------------------------------------------
    # Collapse
    # ----------------------------------------------------

    @classmethod
    def collapse(
        cls,
        payload,
        source="runtime",
        metadata=None
    ):

        return cls._build(

            entity="collapse",

            semantic_type="warning",

            payload=payload,

            source=source,

            metadata=metadata

        )
