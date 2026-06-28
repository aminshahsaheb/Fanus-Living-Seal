"""
==========================================================
FANUS ONTOLOGY — SCHEMA
==========================================================

Canonical object schemas used by the Fanus ontology.

This module defines the minimum required structure
for every semantic object.

It contains NO runtime logic.

It contains NO validation logic.

Validation is performed by ontology validators.

==========================================================
"""

SCHEMA = {

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    "identity": {

        "required": [

            "name",
            "type",
            "version",
            "stability",
            "mode",
            "intent"

        ],

        "optional": [

            "metadata"

        ]
    },

    # --------------------------------------------------
    # Reflection
    # --------------------------------------------------

    "reflection": {

        "required": [

            "observed_identity",
            "signal_strength",
            "reflection"

        ],

        "optional": [

            "timestamp"

        ]
    },

    # --------------------------------------------------
    # Proposal
    # --------------------------------------------------

    "proposal": {

        "required": [

            "type",
            "action",
            "reason"

        ],

        "optional": [

            "priority",
            "confidence"

        ]
    },

    # --------------------------------------------------
    # Decision
    # --------------------------------------------------

    "decision": {

        "required": [

            "action"

        ],

        "optional": [

            "reason"

        ]
    },

    # --------------------------------------------------
    # Memory Event
    # --------------------------------------------------

    "memory_event": {

        "required": [

            "intent"

        ],

        "optional": [

            "timestamp",
            "payload"

        ]
    },

    # --------------------------------------------------
    # Collapse Report
    # --------------------------------------------------

    "collapse": {

        "required": [

            "collapse_score",
            "alert_level",
            "state"

        ],

        "optional": [

            "frozen",
            "recovery_mode"

        ]
    }

}
