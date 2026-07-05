from fastapi import APIRouter
from pydantic import BaseModel
from fanus.memory.pipeline import MemoryPipeline
from fanus.memory.knowledge_graph import KnowledgeGraph
from fanus.memory.belief_layer import BeliefLayer
from fanus.memory.knowledge_versioning import KnowledgeVersioning

router = APIRouter(prefix="/memory", tags=["memory"])

pipeline = MemoryPipeline()
graph = KnowledgeGraph()
versioning = KnowledgeVersioning()

class StoreRequest(BaseModel):
    content: str
    source: str = "user"
    confidence: float = 1.0

class VersionRequest(BaseModel):
    key: str
    content: str
    confidence: float = 1.0

@router.post("/store")
def store(req: StoreRequest):
    result = pipeline.process(req.content, req.source, req.confidence)
    return result

@router.get("/ledger")
def get_ledger():
    return {"entries": pipeline.ledger.get_all()[-20:], "size": pipeline.ledger.size()}

@router.get("/beliefs")
def get_beliefs():
    return {"stats": pipeline.beliefs.stats()}

@router.get("/graph")
def get_graph():
    return graph.snapshot()

@router.post("/version")
def add_version(req: VersionRequest):
    return versioning.add(req.key, req.content, req.confidence)

@router.get("/version/{key}")
def get_version(key: str):
    return {"latest": versioning.latest(key), "history": versioning.history(key)}
