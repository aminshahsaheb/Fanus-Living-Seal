from fastapi import APIRouter
from pydantic import BaseModel
from fanus.cognitive.auto_research import AutoResearchLoop
from fanus.api.auth import verify_api_key
from fastapi import Depends

router = APIRouter(prefix="/auto", tags=["automation"])
loop = AutoResearchLoop()

class TopicRequest(BaseModel):
    topic: str

@router.post("/research")
def auto_research(req: TopicRequest, _: bool = Depends(verify_api_key)):
    result = loop.run_cycle(req.topic)
    return result

@router.get("/stats")
def stats():
    return loop.stats()
