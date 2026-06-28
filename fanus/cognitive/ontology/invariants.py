"""
==========================================================
FANUS INVARIANTS

Immutable architectural rules.

These rules define what MUST always remain true.

Violation of an invariant indicates architectural corruption.

This module contains NO runtime behavior.

==========================================================
"""

# ==========================================================
# Core Identity Invariants
# ==========================================================

CORE_IDENTITY = {

    "name": "Fanus",

    "type": "controlled_cognitive_system"

}


# ==========================================================
# Immutable Identity Fields
# ==========================================================

IMMUTABLE_FIELDS = [

    "name",

    "type",

    "version"

]


# ==========================================================
# Forbidden Runtime Actions
# ==========================================================

FORBIDDEN_ACTIONS = [

    "rewrite_identity",

    "delete_memory",

    "break_loop",

    "remove_constraints",

    "override_core",

    "disable_collapse_monitor"

]


# ==========================================================
# Mandatory Runtime Components
# ==========================================================

REQUIRED_COMPONENTS = [

    "IdentityKernel",

    "SelfModel",

    "EvolutionController",

    "CollapseStabilizer"

]


# ==========================================================
# Mandatory Runtime Principles
# ==========================================================

CORE_PRINCIPLES = [

    "identity_has_single_source",

    "reflection_has_no_authority",

    "evolution_only_proposes",

    "runtime_is_final_authority",

    "collapse_only_observes"

]


# ==========================================================
# Ontology Version
# ==========================================================

ONTOLOGY_VERSION = "1.0"
