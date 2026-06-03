class AutonomyBoundary:
    """
    V5.32.0 — System Autonomy Boundary Layer

    هدف:
    تعریف محدوده تصمیم‌گیری سیستم و جلوگیری از self-expansion غیرقابل کنترل
    """

    def __init__(self):

        # ─────────────────────────────
        # AUTONOMY LEVELS
        # ─────────────────────────────
        self.levels = {
            "L0": "observation_only",
            "L1": "controlled_decision",
            "L2": "calibration_allowed",
            "L3": "rewrite_proposals_only"
        }

        self.current_level = "L2"

        # ─────────────────────────────
        # FORBIDDEN ZONES
        # ─────────────────────────────
        self.forbidden_actions = [
            "auto_delete_core_modules",
            "unbounded_self_modification",
            "bypass_governor",
            "disable_observer"
        ]

    def check_action(self, action: str, context: dict):

        # ─────────────────────────────
        # 1. FORBIDDEN ACTION CHECK
        # ─────────────────────────────
        if action in self.forbidden_actions:
            return {
                "allowed": False,
                "reason": "action is outside autonomy boundary"
            }

        # ─────────────────────────────
        # 2. LEVEL-BASED PERMISSION
        # ─────────────────────────────
        if self.current_level == "L0":
            allowed = action == "observe"

        elif self.current_level == "L1":
            allowed = action in ["observe", "decide"]

        elif self.current_level == "L2":
            allowed = action in ["observe", "decide", "calibrate"]

        elif self.current_level == "L3":
            allowed = action in [
                "observe",
                "decide",
                "calibrate",
                "propose_rewrite"
            ]

        else:
            allowed = False

        # ─────────────────────────────
        # 3. DRIFT SAFETY OVERRIDE
        # ─────────────────────────────
        drift = context.get("drift", 0.0)

        if drift > 0.7:
            return {
                "allowed": False,
                "reason": "system in unstable drift state"
            }

        # ─────────────────────────────
        # 4. OUTPUT
        # ─────────────────────────────
        return {
            "allowed": allowed,
            "level": self.current_level,
            "action": action
        }
