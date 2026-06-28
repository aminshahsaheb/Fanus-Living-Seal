"""
==========================================================
FANUS ONTOLOGY — AUTHORITY
==========================================================

Defines authority boundaries between ontology entities.

Authority is immutable.

Runtime must obey these permissions.

==========================================================
"""

AUTHORITY = {

    "identity": {

        "may_modify": [],

        "may_observe": [],

        "protected": True
    },

    "self_model": {

        "may_modify": [],

        "may_observe": [
            "identity",
            "memory"
        ],

        "protected": False
    },

    "memory": {

        "may_modify": [
            "memory"
        ],

        "may_observe": [
            "event"
        ],

        "protected": False
    },

    "evolution": {

        "may_modify": [
            "proposal"
        ],

        "may_observe": [
            "identity",
            "memory",
            "reflection"
        ],

        "protected": False
    },

    "execution": {

        "may_modify": [
            "event"
        ],

        "may_observe": [
            "proposal"
        ],

        "protected": False
    },

    "collapse": {

        "may_modify": [],

        "may_observe": [
            "identity",
            "evolution"
        ],

        "protected": True
    }

}
