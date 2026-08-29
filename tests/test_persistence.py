import os
from fanus.memory.pipeline import MemoryPipeline


def test_ledger_persists_across_instances(tmp_path, monkeypatch):
    """F-08 regression: ledger/beliefs must survive a fresh MemoryPipeline instance,
    proving state is read from disk, not just held in Python memory."""
    state_file = tmp_path / "test_state.json"
    monkeypatch.chdir(tmp_path)

    mp1 = MemoryPipeline()
    mp1.process("test claim one", "test_source", 0.9)
    assert mp1.ledger.size() == 1

    mp2 = MemoryPipeline()
    assert mp2.ledger.size() == 1
    assert mp2.beliefs.stats()["FACT"] + mp2.beliefs.stats()["HYPOTHESIS"] >= 1


def test_persistence_survives_multiple_writes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mp1 = MemoryPipeline()
    mp1.process("claim a", "source_a", 0.9)
    mp1.process("claim b", "source_b", 0.9)

    mp2 = MemoryPipeline()
    assert mp2.ledger.size() == 2
