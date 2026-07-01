"""
==========================================================
FANUS ARCHITECTURE MAP (SINGLE SOURCE OF TRUTH)
==========================================================

This file defines the official system boundaries.

NO module is allowed to bypass this registry.

==========================================================
"""

ARCHITECTURE_MAP = {
    "stable_core": {
        "runtime": [
            "fanus.runtime.loop",
            "fanus.runtime.decision.decision_engine",
            "fanus.runtime.observer.runtime_observer",
        ],
        "cognitive": [
            "fanus.cognitive.identity_kernel",
            "fanus.cognitive.self_model",
            "fanus.cognitive.memory_layer",
        ],
        "execution": [
            "fanus.cognitive.execution_layer",
        ],
    },

    "controlled_evolution": {
        "evolution": [
            "fanus.cognitive.evolution_controller",
            "fanus.cognitive.evolution.signal_aggregator",
            "fanus.cognitive.evolution.evolution_policy",
            "fanus.cognitive.evolution.proposal_builder",
        ],
    },

    "experimental_self_mod": {
        "self_mod": [
            "fanus.cognitive.self_modifying_identity_kernel",
            "fanus.runtime.self_rewrite_engine",
            "fanus.runtime.runtime_compiler_engine",
            "fanus.runtime.self_stabilization_engine",
            "fanus.cognitive.memory_pressure_engine",
            "fanus.cognitive.evolution.proposal_rewriter",
        ],

        "safety": [
            "fanus.runtime.safety.collapse_safety_gate",
        ],
    },
}


def get_layer(module_path: str) -> str:
    for layer, groups in ARCHITECTURE_MAP.items():
        for group, modules in groups.items():
            if module_path in modules:
                return layer
    return "unknown"
