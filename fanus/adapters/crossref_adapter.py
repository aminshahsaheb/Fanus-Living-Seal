import requests


class CrossrefAdapter:

    def __init__(self):
        self.base = "https://api.crossref.org/works"

    def search(self, query, limit=5):
        params = {"query": query, "rows": limit}
        r = requests.get(self.base, params=params)
        items = r.json().get("message", {}).get("items", [])
        return [{
            "title": i.get("title", [""])[0],
            "doi": i.get("DOI"),
            "year": i.get("published", {}).get("date-parts", [[None]])[0][0],
            "authors": [a.get("family","") for a in i.get("author", [])[:3]]
        } for i in items]