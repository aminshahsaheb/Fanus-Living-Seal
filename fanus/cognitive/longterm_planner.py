import time
from fanus.memory.persistence import PersistenceLayer


class LongTermPlanner:

    def __init__(self):
        self.persistence = PersistenceLayer()
        self.plans = self.persistence.get("longterm_plans", [])

    def create(self, vision, milestones, horizon_days=30):
        plan = {
            "id": len(self.plans) + 1,
            "vision": vision,
            "milestones": [{"goal": m, "done": False} for m in milestones],
            "horizon_days": horizon_days,
            "progress": 0.0,
            "created": time.time()
        }
        self.plans.append(plan)
        self._save()
        return plan

    def complete_milestone(self, plan_id, milestone_index):
        for p in self.plans:
            if p["id"] == plan_id:
                if milestone_index < len(p["milestones"]):
                    p["milestones"][milestone_index]["done"] = True
                    done = sum(1 for m in p["milestones"] if m["done"])
                    p["progress"] = round(done / len(p["milestones"]), 2)
                    self._save()
                return p
        return None

    def active(self):
        return [p for p in self.plans if p["progress"] < 1.0]

    def _save(self):
        self.persistence.save({"longterm_plans": self.plans})

    def stats(self):
        return {
            "total": len(self.plans),
            "active": len(self.active())
        }