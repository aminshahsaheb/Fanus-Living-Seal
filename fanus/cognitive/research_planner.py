import time
from fanus.memory.persistence import PersistenceLayer


class ResearchPlanner:

    def __init__(self):
        self.persistence = PersistenceLayer()
        self.plans = self.persistence.get("research_plans", [])

    def create(self, topic, questions, sources=None):
        plan = {
            "id": len(self.plans) + 1,
            "topic": topic,
            "questions": questions,
            "sources": sources or ["arxiv", "crossref", "pubmed", "wikipedia"],
            "status": "pending",
            "findings": [],
            "created": time.time()
        }
        self.plans.append(plan)
        self._save()
        return plan

    def add_finding(self, plan_id, finding, confidence=0.8):
        for p in self.plans:
            if p["id"] == plan_id:
                p["findings"].append({
                    "finding": finding,
                    "confidence": confidence,
                    "timestamp": time.time()
                })
                p["status"] = "in_progress"
                self._save()
                return p
        return None

    def complete(self, plan_id):
        for p in self.plans:
            if p["id"] == plan_id:
                p["status"] = "completed"
                self._save()
                return p
        return None

    def pending(self):
        return [p for p in self.plans if p["status"] == "pending"]

    def _save(self):
        self.persistence.save({"research_plans": self.plans})

    def stats(self):
        return {
            "total": len(self.plans),
            "pending": len(self.pending()),
            "completed": len([p for p in self.plans if p["status"] == "completed"])
        }