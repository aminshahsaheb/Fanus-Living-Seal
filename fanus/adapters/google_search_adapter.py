import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()


class GoogleSearchAdapter:

    def __init__(self):
        self.key = os.environ.get("GOOGLE_API_KEY", "")
        self.cx = os.environ.get("GOOGLE_CX", "")

    def search(self, query, num=5):
        service = build("customsearch", "v1", developerKey=self.key)
        result = service.cse().list(q=query, cx=self.cx, num=num).execute()
        items = result.get("items", [])
        return [{
            "title": i.get("title"),
            "link": i.get("link"),
            "snippet": i.get("snippet")
        } for i in items]