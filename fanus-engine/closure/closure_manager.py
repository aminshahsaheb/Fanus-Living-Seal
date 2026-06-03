class ClosureManager:
    """
    V5.35.0 — Closure Architecture Layer

    هدف:
    قفل کردن معماری در حالت پایدار و جلوگیری از تغییرات ساختاری بی‌نهایت
    """

    def __init__(self):

        # ─────────────────────────────
        # STABILITY THRESHOLD
        # ─────────────────────────────
        self.stability_threshold = 0.85

        # ─────────────────────────────
        # CLOSURE STATE
        # ─────────────────────────────
        self.is_closed = False

        # ─────────────────────────────
        # CHANGE COUNTER
        # ─────────────────────────────
        self.change_count = 0

    def evaluate_system(self, stability_score: float, rewrite_requests: int):

        # ─────────────────────────────
        # 1. TRACK CHANGES
        # ─────────────────────────────
        self.change_count += rewrite_requests

        # ─────────────────────────────
        # 2. CLOSURE CONDITION
        # ─────────────────────────────
        if stability_score >= self.stability_threshold and self.change_count < 3:
            self.is_closed = True

        elif stability_score < self.stability_threshold:
            self.is_closed = False

        # ─────────────────────────────
        # 3. BLOCK STRUCTURAL CHANGES
        # ─────────────────────────────
        if self.is_closed:
            action = "SYSTEM_LOCKED_STABLE_MODE"
        else:
            action = "ALLOW_CONTROLLED_EVOLUTION"

        # ─────────────────────────────
        # 4. OUTPUT
        # ─────────────────────────────
        return {
            "is_closed": self.is_closed,
            "action": action,
            "stability_score": stability_score,
            "change_count": self.change_count
        }
