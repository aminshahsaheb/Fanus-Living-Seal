"""
==========================================================
FANUS SEMANTIC MEMORY
==========================================================

Single semantic memory layer.

Only validated ontology events may enter memory.

==========================================================
"""

from collections import deque

from fanus.cognitive.ontology.event_validator import (
    EventValidator,
)


class MemoryLayer:
    """
    Semantic Event Memory.

    Stores ONLY validated ontology events.
    """

    def __init__(self, max_events=500):

        self.max_events = max_events

        self.events = deque(maxlen=max_events)

    # -------------------------------------------------
    # STORE
    # -------------------------------------------------

    def store(self, event):

        EventValidator.validate(event)

        self.events.append(event)

        return event

    # -------------------------------------------------
    # READ
    # -------------------------------------------------

    def all(self):

        return list(self.events)

    # -------------------------------------------------

    def latest(self):

        if not self.events:
            return None

        return self.events[-1]

    # -------------------------------------------------

    def by_entity(self, entity):

        return [

            e

            for e in self.events

            if e["entity"] == entity

        ]

    # -------------------------------------------------

    def by_semantic_type(self, semantic_type):

        return [

            e

            for e in self.events

            if e["semantic_type"] == semantic_type

        ]

    # -------------------------------------------------

    def clear(self):

        self.events.clear()

    # -------------------------------------------------

    def size(self):

        return len(self.events)

    # -------------------------------------------------

    def statistics(self):

        stats = {}

        for event in self.events:

            entity = event["entity"]

            stats[entity] = stats.get(entity, 0) + 1

        return stats
