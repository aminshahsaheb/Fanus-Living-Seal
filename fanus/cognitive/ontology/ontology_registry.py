"""
==========================================================
FANUS ONTOLOGY REGISTRY
==========================================================

Single registry describing every official ontology object.

This module is the ONLY discovery point for the
Fanus ontology.

Runtime modules must never manually discover ontology
components.

==========================================================
"""

from fanus.cognitive.ontology.ontology_core import (
    IDENTITY_TYPES,
    INTENT,
    MODE,
    PROPOSAL,
    ACTION,
    COLLAPSE,
    DECISION,
)

from fanus.cognitive.ontology.invariants import (
    CORE_IDENTITY,
    FORBIDDEN_ACTIONS,
)

from fanus.cognitive.ontology.semantic_types import (
    SEMANTIC_TYPE,
)

from fanus.cognitive.ontology.entities import (
    ENTITY,
)

from fanus.cognitive.ontology.relations import (
    RELATION,
)

from fanus.cognitive.ontology.authority import (
    AUTHORITY,
)

from fanus.cognitive.ontology.schema import (
    SCHEMA,
)


class OntologyRegistry:
    """
    Single Source of Ontology Metadata.

    This class exposes every ontology definition through
    one unified interface.
    """

    def __init__(self):

        self.registry = {

            "identity_types": IDENTITY_TYPES,

            "intent": INTENT,

            "mode": MODE,

            "proposal": PROPOSAL,

            "action": ACTION,

            "collapse": COLLAPSE,

            "decision": DECISION,

            "semantic_types": SEMANTIC_TYPE,

            "entities": ENTITY,

            "relations": RELATION,

            "authority": AUTHORITY,

            "schema": SCHEMA,

            "core_identity": CORE_IDENTITY,

            "forbidden_actions": FORBIDDEN_ACTIONS
        }

    # --------------------------------------------------
    # Generic Access
    # --------------------------------------------------

    def get(self, name):

        return self.registry.get(name)

    # --------------------------------------------------
    # Registry Keys
    # --------------------------------------------------

    def keys(self):

        return list(self.registry.keys())

    # --------------------------------------------------
    # Registry Snapshot
    # --------------------------------------------------

    def snapshot(self):

        return self.registry.copy()

    # --------------------------------------------------
    # Registry Size
    # --------------------------------------------------

    def size(self):

        return len(self.registry)
