from typing import Dict


class AutonomyBoundary:

    def __init__(self):

        # ─────────────────────────────
        # HARD LIMITS
        # ─────────────────────────────
        self.max_allowed_drift = 0.75
        self.min_trust_required = 0.35

        # اگر trust خیلی پایین باشد → سیستم فلج می‌شود
        self.freeze_threshold = 0.20

    # ─────────────────────────────
    # MAIN CHECK
    # ─────────────────────────────
    def check_action(self, action: str, drift: float, trust: Dict = None) -> Dict:

        if trust is None:
            trust = {"trust_score": 1.0}

        trust_score = trust.get("trust_score", 1.0)

        # ─────────────────────────────
        # 1. HIGH DRIFT LOCK
        # ─────────────────────────────
        if drift > self.max_allowed_drift:

            return {
                "allowed": False,
                "reason": "drift_too_high",
                "mode": "safe_hold"
            }

        # ─────────────────────────────
        # 2. LOW TRUST LOCK
        # ─────────────────────────────
        if trust_score < self.min_trust_required:

            return {
                "allowed": False,
                "reason": "trust_too_low",
                "mode": "self_repair_required"
            }

        # ─────────────────────────────
        # 3. CRITICAL FREEZE STATE
        # ─────────────────────────────
        if trust_score < self.freeze_threshold:

            return {
                "allowed": False,
                "reason": "system_freeze",
                "mode": "frozen"
            }

        # ─────────────────────────────
        # 4. NORMAL OPERATION
        # ─────────────────────────────
        return {
            "allowed": True,
            "reason": "within_safe_bounds",
            "mode": "active"
        }
