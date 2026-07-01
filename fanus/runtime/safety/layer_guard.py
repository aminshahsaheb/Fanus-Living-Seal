"""
==========================================================
FANUS LAYER GUARD
==========================================================

Prevents illegal cross-layer execution.

Example:
- self-mod cannot directly modify stable_core
- evolution cannot bypass runtime

==========================================================
"""

from fanus.core.architecture_map import ARCHITECTURE_MAP


class LayerGuard:

    def __init__(self):
        self.map = ARCHITECTURE_MAP

    def validate_access(self, source_layer: str, target_module: str) -> bool:

        # stable core is protected
        if source_layer == "experimental_self_mod" and target_module in self._stable_modules():
            return False

        return True

    def _stable_modules(self):
        return self.map["stable_core"]["runtime"] + \
               self.map["stable_core"]["cognitive"] + \
               self.map["stable_core"]["execution"]

    def enforce(self, source_layer: str, target_module: str):

        if not self.validate_access(source_layer, target_module):
            raise PermissionError(
                f"Layer violation: {source_layer} cannot access {target_module}"
            )
