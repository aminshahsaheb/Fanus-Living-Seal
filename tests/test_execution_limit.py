from fanus.cognitive.execution_layer import FanusExecutionLayer


def test_execution_limit_caps_proposals_processed():
    """F-12 regression: execution_limit must actually cap how many proposals run per call."""
    layer = FanusExecutionLayer()
    result = layer.execute({
        "proposals": ["action_a", "action_b", "action_c"],
        "execution_limit": 1
    })
    assert result["events_this_tick"] == 1
    assert result["deferred_this_tick"] == 2
    assert layer.statistics()["applied"] == 1


def test_execution_limit_five_processes_all_when_under_limit():
    layer = FanusExecutionLayer()
    result = layer.execute({
        "proposals": ["action_a", "action_b"],
        "execution_limit": 5
    })
    assert result["events_this_tick"] == 2
    assert result["deferred_this_tick"] == 0


def test_execution_limit_zero_blocks_everything():
    """Collapse severe (collapse > 0.7) maps to execution_limit=1 in self_stabilization_engine,
    but defensively verify limit=0 truly executes nothing."""
    layer = FanusExecutionLayer()
    result = layer.execute({
        "proposals": ["action_a", "action_b"],
        "execution_limit": 0
    })
    assert result["events_this_tick"] == 0
    assert result["deferred_this_tick"] == 2


def test_single_decision_backward_compatible():
    """Old callers passing a single 'decision' string (no proposals list) must still work."""
    layer = FanusExecutionLayer()
    result = layer.execute({"decision": "some_action", "execution_limit": 1})
    assert result["payload"]["action"] == "some_action"
    assert result["payload"]["status"] == "executed"


def test_forbidden_action_still_rejected():
    layer = FanusExecutionLayer()
    result = layer.execute({"decision": "delete_memory", "execution_limit": 1})
    assert result["payload"]["status"] == "rejected"
    assert layer.statistics()["rejected"] == 1
