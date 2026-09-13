# fanus-engine/control/action_router.py

class ActionRouter:

    def route(self, risk_level: str):

        if risk_level == "STABLE":
            return "CONTINUE"

        if risk_level == "WATCH":
            return "LOG_ONLY"

        if risk_level == "HIGH":
            return "REALIGN"

        if risk_level == "CRITICAL":
            return "HALT_AND_AUDIT"
