import wikipediaapi


class WikipediaAdapter:

    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(language="en", user_agent="Fanus/1.0")

    def search(self, query):
        page = self.wiki.page(query)
        if not page.exists():
            return None
        return {
            "title": page.title,
            "summary": page.summary[:300],
            "url": page.fullurl
        }