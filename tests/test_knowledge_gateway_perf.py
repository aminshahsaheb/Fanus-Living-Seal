import time
from fanus.adapters.knowledge_gateway import KnowledgeGateway


def test_search_all_returns_all_six_sources():
    """F-39 regression: parallelization must not drop any source."""
    gw = KnowledgeGateway()
    results = gw.search_all("test query")
    assert set(results.keys()) == {"arxiv", "crossref", "pubmed", "wikipedia", "github", "hn"}


def test_search_all_runs_concurrently_not_sequentially():
    """F-39 regression: verifies PARALLELISM directly (not a fixed-seconds
    threshold, which is fragile against real network variance). Measures
    each adapter's OWN duration when run inside search_all's thread pool
    (via monkeypatching) and compares the total wall-clock time against
    the sum vs. the max of those durations."""
    import unittest.mock as mock
    gw = KnowledgeGateway()

    durations = {}
    real_arxiv = gw.arxiv.search
    real_crossref = gw.crossref.search
    real_pubmed = gw.pubmed.search
    real_wikipedia = gw.wikipedia.search
    real_github = gw.github.search_repos
    real_hn = gw.hn.search

    def wrap(name, fn):
        def inner(*args, **kwargs):
            start = time.time()
            try:
                return fn(*args, **kwargs)
            finally:
                durations[name] = time.time() - start
        return inner

    gw.arxiv.search = wrap("arxiv", real_arxiv)
    gw.crossref.search = wrap("crossref", real_crossref)
    gw.pubmed.search = wrap("pubmed", real_pubmed)
    gw.wikipedia.search = wrap("wikipedia", real_wikipedia)
    gw.github.search_repos = wrap("github", real_github)
    gw.hn.search = wrap("hn", real_hn)

    start = time.time()
    gw.search_all("test query")
    total = time.time() - start

    sum_of_all = sum(durations.values())
    max_single = max(durations.values())

    # If truly parallel, total should be close to the slowest single
    # adapter (+ some overhead), NOT anywhere near the sum of all six.
    # Allow generous overhead (3s) for thread scheduling / GIL contention.
    assert total < max_single + 3.0, (
        f"total={total:.2f}s but max single adapter={max_single:.2f}s "
        f"(sum of all={sum_of_all:.2f}s) -- looks sequential, not parallel"
    )


def test_quick_search_still_works():
    gw = KnowledgeGateway()
    result = gw.quick_search("test")
    assert "total_results" in result
    assert "sources" in result
