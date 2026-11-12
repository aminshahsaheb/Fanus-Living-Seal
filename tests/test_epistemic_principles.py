"""Principles from the continuity research note (docs/CONTINUITY_CLAIM.md), checked against the real pipeline."""
import pytest

from fanus.memory.pipeline import MemoryPipeline


@pytest.mark.parametrize("source", ["user", "fanus", "groq", "blog"])
def test_own_output_and_unsupported_assertions_are_never_facts(source):
    """No component certifies itself: the system's own output and a user's bare assertion stay hypotheses, even at full confidence."""
    assert MemoryPipeline(persist=False).process("Drug X cures every disease", source, 1.0)["belief_type"] != "FACT"


def test_repetition_is_not_evidence():
    p = MemoryPipeline(persist=False)
    seen = {p.process("This supplement cures all diseases", "blog", 0.3)["belief_type"] for _ in range(30)}
    assert seen == {"HYPOTHESIS"}


def test_independent_sources_can_still_support_a_fact():
    """Control: the guards above must not mean that nothing can ever be a FACT."""
    assert MemoryPipeline(persist=False).process("Water boils at 100 C at sea level", "pubmed", 0.9)["belief_type"] == "FACT"


def test_KNOWN_LIMIT_a_declared_source_label_is_trusted_not_verified():
    """Characterisation of a documented gap (CONTINUITY_CLAIM.md, principle 6). When provenance is checked,
    this test should be changed to expect something other than FACT."""
    assert MemoryPipeline(persist=False).process("Water boils at 100 C", "wikipedia", 0.9)["belief_type"] == "FACT"
