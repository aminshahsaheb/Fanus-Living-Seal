class Controller:
    def execute(self, decision: str, state: dict):
        return {
            "decision": decision,
            "action_taken": True,
            "state_snapshot": state
        }
