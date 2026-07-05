from fastapi import APIRouter
from pydantic import BaseModel
from fanus.cognitive.auto_research import AutoResearchLoop

router = APIRouter(prefix="/auto", tags=["automation"])
loop = AutoResearchLoop()

class TopicRequest(BaseModel):
    topic: str

@router.post("/research")
def auto_research(req: TopicRequest):
    result = loop.run_cycle(req.topic)
    return result

@router.get("/stats")
def stats():
    return loop.stats()
