import arxiv


class ArxivAdapter:

    def __init__(self):
        self.client = arxiv.Client()

    def search(self, query, max_results=5):
        search = arxiv.Search(query=query, max_results=max_results)
        results = []
        for r in self.client.results(search):
            results.append({
                "title": r.title,
                "summary": r.summary[:200],
                "authors": [a.name for a in r.authors[:3]],
                "url": r.entry_id,
                "published": str(r.published.date())
            })
        return results