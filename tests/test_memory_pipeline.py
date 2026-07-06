import pytest
from fanus.memory.pipeline import MemoryPipeline

def test_pipeline_accepted():
    mp = MemoryPipeline()
    r = mp.process("زمین گرد است", "NASA", 0.99)
    assert "accepted" in r
    assert "ledger_id" in r

def test_pipeline_rejected():
    mp = MemoryPipeline()
    r = mp.process("زمین مسطح است", "Reddit", 0.05)
    assert r["accepted"] == False

def test_pipeline_belief_type():
    mp = MemoryPipeline()
    r = mp.process("زمین گرد است", "NASA", 0.99)
    assert r["belief_type"] in ["FACT", "HYPOTHESIS", "THEORY", "OPINION"]
