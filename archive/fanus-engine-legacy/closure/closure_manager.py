from typing import Dict


class ClosureManager:

    def __init__(self):

        self.is_closed = False
        self.best_score = 0.0

        # حداقل بهبود لازم برای باز شدن دوباره
        self.improvement_threshold = 0.05

    # ─────────────────────────────
    # MAIN LOGIC
    # ─────────────────────────────
    def evaluate_system(self, stability_score: float, rewrite_requests: int = 0) -> Dict:

        # ─────────────────────────────
        # 1. IMPROVEMENT CHECK
        # ─────────────────────────────
        if stability_score > self.best_score + self.improvement_threshold:

            self.best_score = stability_score
            self.is_closed = False

            return {
                "is_closed": False,
                "mode": "IMPROVEMENT_DETECTED",
                "action": "REOPEN_AND_UPDATE",
                "best_score": self.best_score
            }

        # ─────────────────────────────
        # 2. UPDATE MUTATION MEMORY
        # ─────────────────────────────
        if rewrite_requests > 0:
            self.is_closed = False

        # ─────────────────────────────
        # 3. STABLE LOCK
        # ─────────────────────────────
        self.is_closed = True

        return {
            "is_closed": True,
            "mode": "LOCKED_STABLE_STATE",
            "action": "NO_CHANGE",
            "best_score": self.best_score
        }
