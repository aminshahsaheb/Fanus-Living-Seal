"""
==========================================================
FANUS IDENTITY KERNEL
==========================================================

Single Source of Truth for System Identity

RULES:
- No self-modification
- No external mutation
- No decision making
- No execution logic

Only returns deterministic identity state.

==========================================================
"""

from fanus.cognitive.ontology.ontology_registry import OntologyRegistry

from fanus.cognitive.ontology.invariants import CORE_IDENTITY


class IdentityKernel:
    """
    Identity is immutable at runtime level.

    This kernel only MATERIALIZES identity state
    from Ontology definitions + runtime stability inputs.
    """

    def __init__(self):

        self.registry = OntologyRegistry()

        self.core = CORE_IDENTITY

        self.version = "2.0"

    # =========================================
    # MAIN ENTRYPOINT
    # =========================================
    def evaluate(self, external_state=None):
        """
        Returns canonical identity snapshot.
        """

        stability = self._resolve_stability(external_state)

        mode = self._resolve_mode(stability)

        intent = self._resolve_intent(stability)

        identity = {

            "name": self.core.get("name", "Fanus"),

            "type": self.core.get("type"),

            "version": self.version,

            "stability": stability,

            "mode": mode,

            "intent": intent
        }

        return identity

    # =========================================
    # STABILITY RESOLUTION (SAFE)
    # =========================================
    def _resolve_stability(self, external_state):

        if not external_state:
            return 1.0

        if isinstance(external_state, dict):

            return float(
                external_state.get("stability", 1.0)
            )

        return 1.0

    # =========================================
    # MODE RESOLUTION (ONTOLOGY-BASED)
    # =========================================
    def _resolve_mode(self, stability):

        mode_map = self.registry.get("mode")

        if stability < 0.3:
            return mode_map["RECOVERY"]

        if stability < 0.7:
            return mode_map["BALANCED"]

        return mode_map["STABLE"]

    # =========================================
    # INTENT RESOLUTION (FIXED POLICY)
    # =========================================
    def _resolve_intent(self, stability):

        intent_map = self.registry.get("intent")

        if stability < 0.3:
            return intent_map["RECOVER"]

        if stability < 0.7:
            return intent_map["LEARN"]

        return intent_map["OBSERVE"]
