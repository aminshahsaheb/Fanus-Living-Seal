import warnings
from datetime import datetime, timezone

from fanus.cognitive import policy_engine
from fanus.cognitive.policy_engine import EpistemicSignal, PolicyEngine
from fanus.core import seal_verifier
from fanus.core.seal_verifier import SealVerifier


def test_helper_matches_the_old_utcnow_value_and_format():
    """Same value and the same isoformat() as datetime.utcnow(): naive UTC, no "+00:00" suffix (F-56)."""
    for module in (policy_engine, seal_verifier):
        stamp = module._utcnow()
        assert stamp.tzinfo is None and "+" not in stamp.isoformat()
        assert abs((stamp - datetime.now(timezone.utc).replace(tzinfo=None)).total_seconds()) < 5


def test_policy_and_seal_code_paths_raise_no_deprecation_warning():
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        PolicyEngine().evaluate(EpistemicSignal.HIGH_CONFIDENCE, {"has_evidence": False})
        PolicyEngine().evaluate(EpistemicSignal.UNCERTAINTY_NEEDED, {"has_evidence": False})
        SealVerifier().verify_seal_integrity({"node_id": "n", "seal_hash": "a" * 64, "lineage": [], "covenant_accepted": True})
