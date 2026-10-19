import json

import pytest

from fanus.memory.persistence import PersistenceLayer
from fanus.memory.pipeline import MemoryPipeline


@pytest.fixture(autouse=True)
def isolated_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


def contents(pipeline):
    return [e["content"] for e in pipeline.ledger.get_all()]


def test_non_persistent_pipeline_never_touches_the_state_file(isolated_cwd):
    """F-49: public /demo/* input must stay out of persisted memory."""
    MemoryPipeline(persist=False).process("anonymous visitor", "user", 1.0)
    assert not (isolated_cwd / "fanus_state.json").exists()


def test_anonymous_input_does_not_reach_persisted_memory():
    real = MemoryPipeline()
    real.process("trusted claim", "user", 1.0)
    MemoryPipeline(persist=False).process("anonymous visitor", "user", 1.0)
    assert contents(MemoryPipeline()) == ["trusted claim"]


def test_other_components_saving_other_keys_do_not_wipe_the_ledger():
    """F-49: a component holding a stale copy of the state (e.g. GoalEngine) must not
    overwrite keys it does not own."""
    stale_component = PersistenceLayer()
    pipeline = MemoryPipeline()
    pipeline.process("kept claim", "user", 1.0)
    stale_component.save({"goals": ["new goal"]})
    assert "kept claim" in contents(MemoryPipeline())
    assert PersistenceLayer().get("goals") == ["new goal"]


def test_corrupt_state_file_does_not_crash_startup(isolated_cwd):
    (isolated_cwd / "fanus_state.json").write_text('{"ledger": [ {"id": 1, "sour', encoding="utf-8")
    pipeline = MemoryPipeline()
    assert pipeline.ledger.size() == 0
    assert (isolated_cwd / "fanus_state.json.corrupt").exists()
    pipeline.process("works again", "user", 1.0)
    assert contents(MemoryPipeline()) == ["works again"]


def test_save_is_atomic_and_leaves_no_temp_files(isolated_cwd):
    MemoryPipeline().process("x", "user", 1.0)
    assert [f.name for f in isolated_cwd.iterdir() if ".tmp." in f.name] == []
    json.loads((isolated_cwd / "fanus_state.json").read_text(encoding="utf-8"))
