"""
==========================================================
FANUS EVENT SCHEMA
==========================================================

Canonical semantic event definition.

Every event entering Fanus memory must satisfy
this schema before it can be persisted.

This file contains NO runtime logic.

==========================================================
"""

EVENT_SCHEMA = {

    "required": [

        "entity",

        "semantic_type",

        "timestamp",

        "payload"

    ],

    "optional": [

        "source",

        "metadata"

    ]

}


EVENT_ENTITIES = {

    "identity",

    "reflection",

    "proposal",

    "decision",

    "collapse"

}


EVENT_TYPES = {

    "state",

    "observation",

    "proposal",

    "decision",

    "warning"

}
