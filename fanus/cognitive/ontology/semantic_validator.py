"""
==========================================================
FANUS ONTOLOGY — SEMANTIC VALIDATOR
==========================================================

Semantic validation layer for the Fanus Ontology.

This module validates ontology objects BEFORE
they enter the cognitive system.

It performs NO mutation.

It performs NO correction.

It ONLY accepts or rejects.

==========================================================
"""

from fanus.cognitive.ontology.schema import SCHEMA
from fanus.cognitive.ontology.ontology_core import (
    MODE,
    INTENT,
    PROPOSAL,
    ACTION,
)
from fanus.cognitive.ontology.invariants import (
    FORBIDDEN_ACTIONS,
)


class SemanticValidator:

    """
    Ontology semantic gate.
    """

    # -------------------------------------------------
    # Generic Schema Validation
    # -------------------------------------------------

    def validate_schema(self, object_type: str, data: dict):

        if object_type not in SCHEMA:
            return False, f"Unknown schema: {object_type}"

        required = SCHEMA[object_type]["required"]

        for field in required:

            if field not in data:
                return False, f"Missing field: {field}"

        return True, "OK"

    # -------------------------------------------------
    # Identity Validation
    # -------------------------------------------------

    def validate_identity(self, identity: dict):

        ok, msg = self.validate_schema("identity", identity)

        if not ok:
            return False, msg

        if identity["mode"] not in MODE.values():
            return False, "Invalid identity mode"

        if identity["intent"] not in INTENT.values():
            return False, "Invalid intent"

        if not (0.0 <= identity["stability"] <= 1.0):
            return False, "Invalid stability"

        return True, "VALID"

    # -------------------------------------------------
    # Proposal Validation
    # -------------------------------------------------

    def validate_proposal(self, proposal: dict):

        ok, msg = self.validate_schema("proposal", proposal)

        if not ok:
            return False, msg

        if proposal["type"] not in PROPOSAL.values():
            return False, "Invalid proposal type"

        if proposal["action"] not in ACTION.values():
            return False, "Invalid proposal action"

        if proposal["action"] in FORBIDDEN_ACTIONS:
            return False, "Forbidden action"

        return True, "VALID"

    # -------------------------------------------------
    # Reflection Validation
    # -------------------------------------------------

    def validate_reflection(self, reflection: dict):

        ok, msg = self.validate_schema("reflection", reflection)

        if not ok:
            return False, msg

        signal = reflection["signal_strength"]

        if not (0.0 <= signal <= 1.0):
            return False, "Invalid signal strength"

        return True, "VALID"

    # -------------------------------------------------
    # Collapse Validation
    # -------------------------------------------------

    def validate_collapse(self, collapse: dict):

        ok, msg = self.validate_schema("collapse", collapse)

        if not ok:
            return False, msg

        score = collapse["collapse_score"]

        if not (0.0 <= score <= 1.0):
            return False, "Invalid collapse score"

        return True, "VALID"
