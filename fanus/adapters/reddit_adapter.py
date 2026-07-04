import requests


class RedditAdapter:

    def __init__(self):
        self.base = "https://www.reddit.com"
        self.headers = {"User-Agent": "Fanus/1.0"}

    def search(self, query, limit=5, subreddit="all"):
        url = self.base + "/search.json"
        r = requests.get(url, headers=self.headers, params={
            "q": query, "limit": limit, "sort": "relevance"
        })
        posts = r.json().get("data", {}).get("children", [])
        return [{
            "title": p["data"].get("title"),
            "url": "https://reddit.com" + p["data"].get("permalink",""),
            "score": p["data"].get("score"),
            "subreddit": p["data"].get("subreddit")
        } for p in posts]