from fanus.memory.ledger import MemoryLedger
from fanus.memory.knowledge_graph import KnowledgeGraph
from fanus.memory.evidence_engine import EvidenceEngine
from fanus.memory.scientific_validator import ScientificValidator
from fanus.memory.belief_layer import BeliefLayer
from fanus.memory.source_ranking import SourceRanking


class MemoryPipeline:

    def __init__(self):
        self.ledger = MemoryLedger()
        self.graph = KnowledgeGraph()
        self.evidence = EvidenceEngine()
        self.validator = ScientificValidator()
        self.beliefs = BeliefLayer()
        self.ranking = SourceRanking()

    def process(self, content, source="user", confidence=1.0):
        source_rank = self.ranking.get(source)
        evidence = self.evidence.evaluate(content, [{"source": source, "confidence": confidence}])
        validation = self.validator.validate(content, evidence["confidence"], source_rank)
        belief_type = "FACT" if validation["final_score"] > 0.8 else "HYPOTHESIS"
        self.beliefs.add(content, belief_type, validation["final_score"], source)
        self.graph.add_entity(content, belief_type, validation["final_score"])
        entry = self.ledger.record(source, content, validation["final_score"])
        return {
            "accepted": validation["status"] == "ACCEPTED",
            "belief_type": belief_type,
            "score": validation["final_score"],
            "ledger_id": entry["id"]
        }