import requests


class PubMedAdapter:

    def __init__(self):
        self.search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    def search(self, query, limit=5):
        r = requests.get(self.search_url, params={
            "db": "pubmed", "term": query,
            "retmax": limit, "retmode": "json"
        })
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []
        r2 = requests.get(self.fetch_url, params={
            "db": "pubmed", "id": ",".join(ids), "retmode": "json"
        })
        uids = r2.json().get("result", {}).get("uids", [])
        result = r2.json().get("result", {})
        return [{
            "title": result[uid].get("title"),
            "year": result[uid].get("pubdate", "")[:4],
            "url": "https://pubmed.ncbi.nlm.nih.gov/" + uid
        } for uid in uids]