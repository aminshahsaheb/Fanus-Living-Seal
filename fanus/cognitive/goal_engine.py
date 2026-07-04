import time
from fanus.memory.persistence import PersistenceLayer


class GoalEngine:

    def __init__(self):
        self.persistence = PersistenceLayer()
        self.goals = self.persistence.get("goals", [])

    def add(self, goal, priority=1.0, source="user"):
        g = {
            "id": len(self.goals) + 1,
            "goal": goal,
            "priority": priority,
            "source": source,
            "status": "active",
            "created": time.time()
        }
        self.goals.append(g)
        self._save()
        return g

    def complete(self, goal_id):
        for g in self.goals:
            if g["id"] == goal_id:
                g["status"] = "completed"
                self._save()
                return g
        return None

    def active(self):
        return [g for g in self.goals if g["status"] == "active"]

    def top(self):
        active = self.active()
        if not active:
            return None
        return max(active, key=lambda g: g["priority"])

    def _save(self):
        self.persistence.save({"goals": self.goals})

    def stats(self):
        return {
            "total": len(self.goals),
            "active": len(self.active()),
            "completed": len([g for g in self.goals if g["status"] == "completed"])
        }