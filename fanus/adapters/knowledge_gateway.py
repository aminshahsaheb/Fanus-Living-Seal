from fanus.adapters.arxiv_adapter import ArxivAdapter
from fanus.adapters.crossref_adapter import CrossrefAdapter
from fanus.adapters.pubmed_adapter import PubMedAdapter
from fanus.adapters.wikipedia_adapter import WikipediaAdapter
from fanus.adapters.github_adapter import GitHubAdapter
from fanus.adapters.hackernews_adapter import HackerNewsAdapter


from concurrent.futures import ThreadPoolExecutor


class KnowledgeGateway:

    def __init__(self):
        self.arxiv = ArxivAdapter()
        self.crossref = CrossrefAdapter()
        self.pubmed = PubMedAdapter()
        self.wikipedia = WikipediaAdapter()
        self.github = GitHubAdapter()
        self.hn = HackerNewsAdapter()

    def search_all(self, query, limit=3):
        # F-39: was sequential (6 blocking HTTP calls back to back, ~10s+
        # total). Now runs all six adapters concurrently in threads so
        # total time is roughly the SLOWEST single adapter, not the sum.
        jobs = {
            "arxiv": (lambda: self.arxiv.search(query, limit), []),
            "crossref": (lambda: self.crossref.search(query, limit), []),
            "pubmed": (lambda: self.pubmed.search(query, limit), []),
            "wikipedia": (lambda: self.wikipedia.search(query), None),
            "github": (lambda: self.github.search_repos(query, limit), []),
            "hn": (lambda: self.hn.search(query, limit), []),
        }
        results = {}
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {name: executor.submit(fn) for name, (fn, _default) in jobs.items()}
            for name, future in futures.items():
                _fn, default = jobs[name]
                try:
                    results[name] = future.result(timeout=8)
                except Exception:
                    results[name] = default
        return results

    def quick_search(self, query):
        results = self.search_all(query, limit=2)
        total = sum(len(v) if isinstance(v, list) else (1 if v else 0) for v in results.values())
        return {"query": query, "total_results": total, "sources": list(results.keys())}