"""
==========================================================
FANUS ONTOLOGY — RELATIONS
==========================================================

Formal relationships between ontology entities.

This file defines which entities are allowed
to observe, influence, reference or constrain
other entities.

No runtime logic.

No execution.

Only semantic structure.

==========================================================
"""

RELATION = {

    # -----------------------------------------
    # Identity
    # -----------------------------------------

    "IDENTITY": {

        "observes": [],

        "influences": [],

        "referenced_by": [

            "self_model",

            "runtime",

            "boundary",

            "collapse",

            "evolution"

        ]
    },

    # -----------------------------------------
    # Self Model
    # -----------------------------------------

    "self_model": {

        "observes": [

            "identity"

        ],

        "influences": [],

        "referenced_by": [

            "meta_self_model",

            "evolution"

        ]
    },

    # -----------------------------------------
    # Meta Self
    # -----------------------------------------

    "meta_self_model": {

        "observes": [

            "self_model"

        ],

        "influences": [],

        "referenced_by": [

            "evolution"

        ]
    },

    # -----------------------------------------
    # Memory
    # -----------------------------------------

    "memory": {

        "observes": [

            "event"

        ],

        "influences": [],

        "referenced_by": [

            "self_model",

            "runtime"

        ]
    },

    # -----------------------------------------
    # Evolution
    # -----------------------------------------

    "evolution": {

        "observes": [

            "identity",

            "self_model",

            "memory"

        ],

        "influences": [

            "proposal"

        ],

        "referenced_by": [

            "runtime"

        ]
    },

    # -----------------------------------------
    # Execution
    # -----------------------------------------

    "execution": {

        "observes": [

            "proposal"

        ],

        "influences": [

            "event"

        ],

        "referenced_by": [

            "runtime"

        ]
    }
}
