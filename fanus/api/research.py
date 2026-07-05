from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from fanus.cognitive.research_planner import ResearchPlanner
from fanus.cognitive.curiosity_engine import CuriosityEngine
from fanus.adapters.knowledge_gateway import KnowledgeGateway

router = APIRouter(prefix="/research", tags=["research"])

planner = ResearchPlanner()
curiosity = CuriosityEngine()
gateway = KnowledgeGateway()

class PlanRequest(BaseModel):
    topic: str
    questions: List[str] = []

class SearchRequest(BaseModel):
    query: str
    limit: int = 3

@router.post("/plan")
def create_plan(req: PlanRequest):
    questions = req.questions or curiosity.generate(req.topic)
    q_list = [q["question"] for q in questions] if isinstance(questions[0], dict) else questions
    plan = planner.create(req.topic, q_list)
    return plan

@router.post("/search")
def search(req: SearchRequest):
    results = gateway.quick_search(req.query)
    return results

@router.get("/plans")
def get_plans():
    return {"plans": planner.plans, "stats": planner.stats()}

@router.get("/curiosity")
def get_curiosity():
    return {"unanswered": curiosity.unanswered()[:5], "stats": curiosity.stats()}
