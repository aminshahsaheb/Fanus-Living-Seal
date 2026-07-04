import requests


class HackerNewsAdapter:

    def __init__(self):
        self.base = "https://hn.algolia.com/api/v1"

    def search(self, query, limit=5):
        r = requests.get(self.base + "/search", params={
            "query": query,
            "tags": "story",
            "hitsPerPage": limit
        })
        hits = r.json().get("hits", [])
        return [{
            "title": h.get("title"),
            "url": h.get("url"),
            "points": h.get("points"),
            "author": h.get("author"),
            "created": h.get("created_at", "")[:10]
        } for h in hits]