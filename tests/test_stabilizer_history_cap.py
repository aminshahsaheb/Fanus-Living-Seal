from fanus.runtime.self_stabilization_engine import SelfStabilizationEngine


def test_history_capped_at_500():
    """F-40 regression: history must not grow unbounded on a long-running
    server (previously appended forever, never read back by anything)."""
    engine = SelfStabilizationEngine()
    for _ in range(600):
        engine.evaluate({"meta": {"collapse_score": 0.1}}, {"meta": {"stability": 1.0}})
    assert len(engine.history) == 500


def test_history_still_works_under_cap():
    engine = SelfStabilizationEngine()
    for _ in range(10):
        engine.evaluate({"meta": {"collapse_score": 0.1}}, {"meta": {"stability": 1.0}})
    assert len(engine.history) == 10
