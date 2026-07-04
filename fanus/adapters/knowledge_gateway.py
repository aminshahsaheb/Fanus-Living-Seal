from fanus.adapters.arxiv_adapter import ArxivAdapter
from fanus.adapters.crossref_adapter import CrossrefAdapter
from fanus.adapters.pubmed_adapter import PubMedAdapter
from fanus.adapters.wikipedia_adapter import WikipediaAdapter
from fanus.adapters.github_adapter import GitHubAdapter
from fanus.adapters.hackernews_adapter import HackerNewsAdapter


class KnowledgeGateway:

    def __init__(self):
        self.arxiv = ArxivAdapter()
        self.crossref = CrossrefAdapter()
        self.pubmed = PubMedAdapter()
        self.wikipedia = WikipediaAdapter()
        self.github = GitHubAdapter()
        self.hn = HackerNewsAdapter()

    def search_all(self, query, limit=3):
        results = {}
        try:
            results["arxiv"] = self.arxiv.search(query, limit)
        except:
            results["arxiv"] = []
        try:
            results["crossref"] = self.crossref.search(query, limit)
        except:
            results["crossref"] = []
        try:
            results["pubmed"] = self.pubmed.search(query, limit)
        except:
            results["pubmed"] = []
        try:
            results["wikipedia"] = self.wikipedia.search(query)
        except:
            results["wikipedia"] = None
        try:
            results["github"] = self.github.search_repos(query, limit)
        except:
            results["github"] = []
        try:
            results["hn"] = self.hn.search(query, limit)
        except:
            results["hn"] = []
        return results

    def quick_search(self, query):
        results = self.search_all(query, limit=2)
        total = sum(len(v) if isinstance(v, list) else (1 if v else 0) for v in results.values())
        return {"query": query, "total_results": total, "sources": list(results.keys())}