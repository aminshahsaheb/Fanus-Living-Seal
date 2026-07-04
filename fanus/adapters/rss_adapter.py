import feedparser


class RSSAdapter:

    FEEDS = {
        "nature": "https://www.nature.com/nature.rss",
        "arxiv_ai": "https://rss.arxiv.org/rss/cs.AI",
        "science": "https://www.science.org/rss/news_current.xml",
        "mit_news": "https://news.mit.edu/rss/research"
    }

    def __init__(self):
        pass

    def fetch(self, source="arxiv_ai", limit=5):
        url = self.FEEDS.get(source, source)
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries[:limit]:
            results.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", "")[:200],
                "link": entry.get("link", ""),
                "published": entry.get("published", "")
            })
        return results

    def available_feeds(self):
        return list(self.FEEDS.keys())