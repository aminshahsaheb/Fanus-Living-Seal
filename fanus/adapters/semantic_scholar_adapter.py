import requests


class SemanticScholarAdapter:

    def __init__(self):
        self.base = "https://api.semanticscholar.org/graph/v1"

    def search(self, query, limit=5):
        url = self.base + "/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,abstract,url"
        }
        r = requests.get(url, params=params)
        papers = r.json().get("data", [])
        return [{
            "title": p.get("title"),
            "year": p.get("year"),
            "authors": [a["name"] for a in p.get("authors", [])[:3]],
            "abstract": (p.get("abstract") or "")[:200],
            "url": p.get("url")
        } for p in papers]