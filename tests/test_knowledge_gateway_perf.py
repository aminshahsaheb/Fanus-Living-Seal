import time
from fanus.adapters.knowledge_gateway import KnowledgeGateway


def test_search_all_returns_all_six_sources():
    """F-39 regression: parallelization must not drop any source."""
    gw = KnowledgeGateway()
    results = gw.search_all("test query")
    assert set(results.keys()) == {"arxiv", "crossref", "pubmed", "wikipedia", "github", "hn"}


def test_search_all_completes_reasonably_fast():
    """F-39 regression: was sequential (~10s+), must now run in parallel
    (bounded by the slowest single adapter, not the sum of all six)."""
    gw = KnowledgeGateway()
    start = time.time()
    gw.search_all("test query")
    elapsed = time.time() - start
    assert elapsed < 9.0, f"search_all took {elapsed}s — looks sequential again, not parallel"


def test_quick_search_still_works():
    gw = KnowledgeGateway()
    result = gw.quick_search("test")
    assert "total_results" in result
    assert "sources" in result
