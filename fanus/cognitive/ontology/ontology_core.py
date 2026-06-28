"""
==========================================================
FANUS ONTOLOGY CORE
==========================================================

Single Source of Meaning

This module defines the official semantic vocabulary
used throughout the Fanus architecture.

It contains NO runtime logic.

It contains NO decision making.

It contains NO state mutation.

Every cognitive module must reference these definitions
instead of creating its own meanings.

==========================================================
"""


# ==========================================================
# Identity Types
# ==========================================================

IDENTITY_TYPES = {

    "CONTROLLED_SYSTEM": "controlled_cognitive_system",

    "WITNESS_SYSTEM": "witness_system",

    "HUMAN_OPERATOR": "human_operator"

}


# ==========================================================
# Intent Types
# ==========================================================

INTENT = {

    "OBSERVE": "neutral_observe",

    "LEARN": "controlled_learning",

    "RECOVER": "stability_recovery",

    "EXPLORE": "bounded_exploration"

}


# ==========================================================
# Identity Modes
# ==========================================================

MODE = {

    "STABLE":

        "stable_core_state",

    "BALANCED":

        "balanced_evolution_state",

    "RECOVERY":

        "recovery_mode"

}


# ==========================================================
# Proposal Types
# ==========================================================

PROPOSAL = {

    "REPAIR":

        "stability_repair",

    "LEARNING":

        "exploration_mode",

    "BOOST":

        "exploration_boost"

}


# ==========================================================
# Proposal Actions
# ==========================================================

ACTION = {

    "REDUCE":

        "reduce_exploration",

    "LEARN":

        "controlled_learning",

    "EXPAND":

        "increase_decision_freedom"

}


# ==========================================================
# Collapse States
# ==========================================================

COLLAPSE = {

    "SAFE":

        "MONITORING_ONLY",

    "WARNING":

        "WARNING",

    "CRITICAL":

        "CRITICAL"

}


# ==========================================================
# Runtime Decisions
# ==========================================================

DECISION = {

    "HALT":

        "HALT_SYSTEM",

    "STABILIZE":

        "ENTER_STABILIZATION_MODE",

    "ALLOW":

        "ALLOW_WITH_CAUTION",

    "NOOP":

        "NOOP"

}
