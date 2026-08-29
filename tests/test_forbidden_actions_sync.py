from fanus.cognitive.execution_layer import FanusExecutionLayer
from fanus.cognitive.ontology.invariants import FORBIDDEN_ACTIONS


def test_execution_layer_uses_single_source_of_truth():
    """F-32 regression: execution_layer._validate() must read from
    invariants.py, not a local hardcoded copy that can silently drift."""
    layer = FanusExecutionLayer()
    for action in FORBIDDEN_ACTIONS:
        result = layer.execute({"decision": action, "execution_limit": 1})
        assert result["payload"]["status"] == "rejected", f"{action} should be forbidden"


def test_remove_constraints_is_blocked():
    """Specific regression: remove_constraints was missing from the old local
    copy in execution_layer.py, meaning it was silently ALLOWED. Must be rejected."""
    layer = FanusExecutionLayer()
    result = layer.execute({"decision": "remove_constraints", "execution_limit": 1})
    assert result["payload"]["status"] == "rejected"


def test_safe_action_still_executes():
    layer = FanusExecutionLayer()
    result = layer.execute({"decision": "some_safe_action", "execution_limit": 1})
    assert result["payload"]["status"] == "executed"
