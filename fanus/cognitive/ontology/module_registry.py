"""
==========================================================
FANUS MODULE REGISTRY (ONTOLOGY LEVEL)
==========================================================

Every module must be registered here.

This is the semantic truth layer for system structure.

==========================================================
"""

from fanus.core.architecture_map import ARCHITECTURE_MAP


class ModuleRegistry:

    def __init__(self):
        self.registry = ARCHITECTURE_MAP

    def get_all_modules(self):
        modules = []
        for layer in self.registry.values():
            for group in layer.values():
                modules.extend(group)
        return modules

    def is_valid_module(self, module_path: str) -> bool:
        return module_path in self.get_all_modules()

    def describe(self):
        return {
            "total_modules": len(self.get_all_modules()),
            "layers": list(self.registry.keys()),
            "status": "canonical"
        }
