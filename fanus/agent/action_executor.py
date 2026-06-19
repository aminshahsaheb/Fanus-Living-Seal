class ActionExecutor:

    def __init__(self):
        self.last_action = None

    def execute(self, action):
        self.last_action = action

        return {
            "status": "ok",
            "executed": action
        }
