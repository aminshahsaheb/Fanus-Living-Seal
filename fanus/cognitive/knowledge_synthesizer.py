import time
from fanus.memory.pipeline import MemoryPipeline
from fanus.memory.knowledge_compression import KnowledgeCompression
from fanus.memory.conflict_resolver import ConflictResolver
from fanus.memory.source_ranking import SourceRanking


class KnowledgeSynthesizer:

    def __init__(self):
        self.compression = KnowledgeCompression()
        self.resolver = ConflictResolver()
        self.ranking = SourceRanking()
        self.syntheses = []

    def synthesize(self, topic, claims):
        ranked = sorted(claims, key=lambda c: self.ranking.get(c.get("source","unknown")), reverse=True)
        compressed = self.compression.compress(topic, ranked)
        conflicts = []
        for i in range(len(ranked)):
            for j in range(i+1, len(ranked)):
                if ranked[i].get("content","") != ranked[j].get("content",""):
                    r = self.resolver.add(
                        ranked[i].get("content",""),
                        ranked[i].get("source","unknown"),
                        ranked[i].get("confidence",0.5),
                        ranked[j].get("content",""),
                        ranked[j].get("source","unknown"),
                        ranked[j].get("confidence",0.5)
                    )
                    if r["resolved"]:
                        conflicts.append(r["winner"])
        result = {
            "topic": topic,
            "claim_count": len(claims),
            "avg_confidence": compressed["avg_confidence"] if compressed else 0,
            "summary": compressed["summary"] if compressed else "",
            "conflicts_resolved": len(conflicts),
            "timestamp": time.time()
        }
        self.syntheses.append(result)
        return result

    def stats(self):
        return {"total_syntheses": len(self.syntheses)}
