import pytest
from unittest.mock import patch
from fanus.runtime.loop import FanusLoop


def test_governance_locked_blocks_execution():
    """F-10/F-11 regression test: a locked governance decision must prevent execution."""
    loop = FanusLoop()
    with patch.object(loop.hard_guard, "evaluate", return_value={"allowed": True, "reason": None}), \
         patch.object(loop.governor, "evaluate", return_value={"locked": True, "autonomy_level": "none"}), \
         patch.object(loop.execution, "execute") as mock_execute:
        loop._tick()
        mock_execute.assert_not_called()


def test_governance_unlocked_allows_execution():
    """Sanity check: when governance is not locked, execution should still run."""
    loop = FanusLoop()
    with patch.object(loop.hard_guard, "evaluate", return_value={"allowed": True, "reason": None}), \
         patch.object(loop.governor, "evaluate", return_value={"locked": False, "autonomy_level": "full"}), \
         patch.object(loop.execution, "execute", return_value={"status": "ok"}) as mock_execute:
        loop._tick()
        mock_execute.assert_called_once()
