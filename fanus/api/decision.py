from fastapi import APIRouter
from pydantic import BaseModel
from fanus.cognitive.goal_engine import GoalEngine
from fanus.cognitive.longterm_planner import LongTermPlanner
from fanus.cognitive.self_review import SelfReview
from fanus.cognitive.autonomy_governor import FanusAutonomyGovernor

router = APIRouter(prefix="/decision", tags=["decision"])

goals = GoalEngine()
planner = LongTermPlanner()
review = SelfReview()
governor = FanusAutonomyGovernor()

class GoalRequest(BaseModel):
    goal: str
    priority: float = 1.0

class PlanRequest(BaseModel):
    vision: str
    milestones: list
    horizon_days: int = 30

@router.post("/goal")
def add_goal(req: GoalRequest):
    return goals.add(req.goal, req.priority)

@router.get("/goals")
def get_goals():
    return {"active": goals.active(), "top": goals.top(), "stats": goals.stats()}

@router.post("/plan")
def create_plan(req: PlanRequest):
    return planner.create(req.vision, req.milestones, req.horizon_days)

@router.get("/plans")
def get_plans():
    return {"plans": planner.active(), "stats": planner.stats()}

@router.get("/review")
def get_review():
    r = review.review(
        goals.goals,
        [],
        goals.active(),
        planner.active()
    )
    return r

@router.get("/governance")
def get_governance():
    return governor.evaluate(
        {"stability": 1.0, "drift": 0.0},
        {"stability": 1.0},
        {"collapse_score": 0.0}
    )
