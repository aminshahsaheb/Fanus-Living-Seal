class SourceRanking:

    RANKS = {
        "Nature": 1.0,
        "Science": 1.0,
        "PubMed": 0.95,
        "ArXiv": 0.85,
        "Crossref": 0.8,
        "SemanticScholar": 0.8,
        "Wikipedia": 0.7,
        "GitHub": 0.65,
        "HackerNews": 0.5,
        "Reddit": 0.3,
        "unknown": 0.1
    }

    def __init__(self):
        self.custom = {}

    def get(self, source):
        if source in self.custom:
            return self.custom[source]
        for key in self.RANKS:
            if key.lower() in source.lower():
                return self.RANKS[key]
        return self.RANKS["unknown"]

    def add_custom(self, source, rank):
        self.custom[source] = min(max(rank, 0.0), 1.0)

    def compare(self, source_a, source_b):
        a = self.get(source_a)
        b = self.get(source_b)
        if a > b:
            return source_a
        elif b > a:
            return source_b
        return "equal"