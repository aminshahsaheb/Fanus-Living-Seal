import requests
import os
from dotenv import load_dotenv

load_dotenv()


class GitHubAdapter:

    def __init__(self):
        self.token = os.environ.get("GITHUB_TOKEN", "")
        self.headers = {"Authorization": "Bearer " + self.token} if self.token else {}
        self.base = "https://api.github.com"

    def search_repos(self, query, limit=5):
        r = requests.get(self.base + "/search/repositories",
            headers=self.headers,
            params={"q": query, "per_page": limit, "sort": "stars"}
        )
        items = r.json().get("items", [])
        return [{
            "name": i["full_name"],
            "description": i.get("description", ""),
            "stars": i["stargazers_count"],
            "url": i["html_url"]
        } for i in items]