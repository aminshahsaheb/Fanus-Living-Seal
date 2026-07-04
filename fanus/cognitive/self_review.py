import time
from fanus.memory.persistence import PersistenceLayer


class SelfReview:

    def __init__(self):
        self.persistence = PersistenceLayer()
        self.reviews = self.persistence.get("self_reviews", [])

    def review(self, ledger, beliefs, goals, plans):
        ledger_size = len(ledger) if ledger else 0
        belief_count = len(beliefs) if beliefs else 0
        active_goals = len([g for g in goals if g.get("status") == "active"]) if goals else 0
        active_plans = len([p for p in plans if p.get("progress", 0) < 1.0]) if plans else 0
        health = round((min(ledger_size, 100) / 100 * 0.3) +
                       (min(belief_count, 50) / 50 * 0.3) +
                       (min(active_goals, 5) / 5 * 0.2) +
                       (min(active_plans, 3) / 3 * 0.2), 3)
        result = {
            "id": len(self.reviews) + 1,
            "ledger_size": ledger_size,
            "belief_count": belief_count,
            "active_goals": active_goals,
            "active_plans": active_plans,
            "health_score": health,
            "status": "HEALTHY" if health > 0.6 else "GROWING" if health > 0.3 else "EARLY",
            "timestamp": time.time()
        }
        self.reviews.append(result)
        self._save()
        return result

    def latest(self):
        return self.reviews[-1] if self.reviews else None

    def _save(self):
        self.persistence.save({"self_reviews": self.reviews})