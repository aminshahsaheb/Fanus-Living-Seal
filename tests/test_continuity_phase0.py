import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("continuity_phase0", ROOT / "research" / "continuity_phase0.py")
phase0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(phase0)


def test_phase0_matches_its_preregistered_predictions():
    r = phase0.run()
    assert r["hash_baseline_correct"] == phase0.PREDICTED["hash_baseline_correct"]
    assert r["vector_correct"] == phase0.PREDICTED["vector_correct"]
    assert sorted(r["vector_wrong"]) == sorted(phase0.PREDICTED["vector_wrong"])


def test_hash_equality_fails_every_faithful_but_different_transition():
    """The design contains the cases that matter: five faithful transitions whose hashes differ."""
    assert phase0.run()["faithful_but_different"] == 5


def test_a_verdict_does_not_depend_on_what_is_already_stored():
    """Characterisation (F-55): the same probe gets the same verdict with empty memory and with contradicting memory.
    If memory ever starts to influence verdicts, update docs/CONTINUITY_PHASE0.md and this test."""
    assert phase0.memory_independence_probe()["identical"] is True
