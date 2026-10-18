import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("reality_map", ROOT / "scripts" / "reality_map.py")
reality_map = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reality_map)

# F-31: high-risk capabilities that exist in the codebase but must not be wired into
# any production entry point without a deliberate, reviewed decision.
DORMANT_HIGH_RISK = [
    "fanus.tools.git_guard",               # autonomous git add/commit/push
    "fanus.evolution.self_modifying_agent",  # rewrites source files, then commits
    "fanus.evolution.self_improver",       # overwrites files
    "fanus.agent.action_executor",
    "fanus.core.plugin_system",            # dynamic importlib loading
    "fanus.runtime.self_rewrite_engine",
    "fanus.runtime.runtime_compiler_engine",
    "fanus.runtime.safety.collapse_safety_gate",
]


def test_dormant_high_risk_modules_stay_unreachable():
    result = reality_map.compute(str(ROOT))
    wired = [m for m in DORMANT_HIGH_RISK if m in result["union"]]
    assert not wired, (
        f"high-risk modules became reachable from a production entry point: {wired}. "
        "If this is intentional, review the authority chain first (docs/AUDIT_FINDINGS.md F-31) "
        "and update this list."
    )


def test_listed_modules_actually_exist():
    # a typo in the list above would make the guard pass vacuously
    result = reality_map.compute(str(ROOT))
    missing = [m for m in DORMANT_HIGH_RISK if m not in result["real"]]
    assert not missing, f"guard list names modules that do not exist: {missing}"
