import time


class KnowledgeCompression:

    def __init__(self):
        self.compressed = []

    def compress(self, topic, claims):
        if not claims:
            return None
        total_conf = sum(c.get("confidence", 0.0) for c in claims)
        avg_conf = round(total_conf / len(claims), 3)
        sources = list(set(c.get("source", "unknown") for c in claims))
        contents = [c.get("content", "") for c in claims]
        result = {
            "topic": topic,
            "claim_count": len(claims),
            "avg_confidence": avg_conf,
            "sources": sources,
            "summary": contents[0] if len(contents) == 1 else contents[0] + " (+" + str(len(contents)-1) + " more)",
            "timestamp": time.time()
        }
        self.compressed.append(result)
        return result

    def size(self):
        return len(self.compressed)