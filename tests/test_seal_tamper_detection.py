import pytest

from fanus.core.identity import FanusIdentity
from fanus.core.seal_verifier import SealVerifier

STATE = {"node_id": "n1", "seal_hash": "a" * 64, "lineage": ["x"], "covenant_accepted": True}


def stored_hash():
    return SealVerifier().verify_seal_integrity(STATE)["current_hash"]


def test_without_a_baseline_the_verifier_never_says_passed():
    result = SealVerifier().verify_seal_integrity(STATE)
    assert result["integrity_check"] == "BASELINE_ESTABLISHED" and result["current_hash"]


def test_unchanged_state_passes_against_its_stored_hash():
    assert SealVerifier().verify_seal_integrity(STATE, stored_hash())["integrity_check"] == "PASSED"


@pytest.mark.parametrize("change", [{"seal_hash": "b" * 64}, {"lineage": ["x", "intruder"]},
                                    {"covenant_accepted": False}, {"node_id": "n2"}])
def test_any_change_to_the_core_identity_is_detected(change):
    assert SealVerifier().verify_seal_integrity({**STATE, **change}, stored_hash())["integrity_check"] == "FAILED"


def test_identity_verify_no_longer_passes_tampered_state_blindly():
    """F-53: FanusIdentity().verify() used to answer PASSED for any state, tampered or not."""
    identity = FanusIdentity()
    stored = identity.verify(STATE)["current_hash"]
    tampered = {**STATE, "lineage": ["x", "intruder"]}
    assert identity.verify(tampered)["integrity_check"] != "PASSED"
    assert identity.verify(tampered, stored)["integrity_check"] == "FAILED"
    assert identity.verify(STATE, stored)["integrity_check"] == "PASSED"
