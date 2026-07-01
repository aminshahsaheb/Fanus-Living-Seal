"""
==========================================================
FANUS RUNTIME HARD GUARD (FINAL SAFETY LAYER)
==========================================================

This is the FINAL execution boundary.

It can override runtime execution ONLY for safety.

==========================================================
"""

class RuntimeHardGuard:

    def __init__(self):
        self.violation_count = 0
        self.locked = False

    def evaluate(self, collapse_state, execution_state):

        collapse_score = collapse_state.get("collapse_score", 0)

        # ---------------------------------------
        # CRITICAL COLLAPSE LOCK
        # ---------------------------------------
        if collapse_score > 0.85:
            self.locked = True
            return {
                "allowed": False,
                "reason": "CRITICAL_COLLAPSE",
                "execution_limit": 0,
                "tick_delay": 1.0
            }

        # ---------------------------------------
        # WARNING ZONE
        # ---------------------------------------
        if collapse_score > 0.6:
            self.violation_count += 1

        if self.violation_count > 3:
            self.locked = True
            return {
                "allowed": False,
                "reason": "REPEATED_INSTABILITY",
                "execution_limit": 0.2,
                "tick_delay": 0.8
            }

        # ---------------------------------------
        # NORMAL OPERATION
        # ---------------------------------------
        return {
            "allowed": True,
            "reason": "STABLE",
            "execution_limit": 1.0,
            "tick_delay": 0.2
        }

    def reset(self):
        self.violation_count = 0
        self.locked = False
