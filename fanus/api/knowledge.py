from fastapi import APIRouter
from pydantic import BaseModel
from fanus.adapters.knowledge_gateway import KnowledgeGateway
from fanus.memory.pipeline import MemoryPipeline
from fanus.memory.evidence_engine import EvidenceEngine
from fanus.memory.scientific_validator import ScientificValidator
from fanus.memory.knowledge_graph import KnowledgeGraph

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

gateway = KnowledgeGateway()
pipeline = MemoryPipeline()
evidence = EvidenceEngine()
validator = ScientificValidator()
graph = KnowledgeGraph()

class SearchRequest(BaseModel):
    query: str
    limit: int = 3

class ValidateRequest(BaseModel):
    claim: str
    source: str = "unknown"
    confidence: float = 0.8

@router.post("/search")
def search(req: SearchRequest):
    results = gateway.search_all(req.query, req.limit)
    return {"query": req.query, "results": results}

@router.post("/validate")
def validate(req: ValidateRequest):
    result = pipeline.process(req.claim, req.source, req.confidence)
    return result

@router.get("/graph")
def get_graph():
    return graph.snapshot()

@router.get("/beliefs")
def get_beliefs():
    return pipeline.beliefs.stats()
