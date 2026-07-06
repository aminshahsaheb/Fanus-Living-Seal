import pytest
from fanus.cognitive.identity_kernel import IdentityKernel


def test_identity_evaluate_stable():
    ik = IdentityKernel()
    result = ik.evaluate({"stability": 1.0})
    assert result["mode"] == "stable_core_state"
    assert result["stability"] == 1.0


def test_identity_evaluate_recovery():
    ik = IdentityKernel()
    result = ik.evaluate({"stability": 0.2})
    assert result["mode"] == "recovery_mode"


def test_identity_name():
    ik = IdentityKernel()
    result = ik.evaluate()
    assert result["name"] == "Fanus"
