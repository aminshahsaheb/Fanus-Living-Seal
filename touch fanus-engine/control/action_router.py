class ActionRouter:

    def route(self, policy_result):

        if policy_result == "stable":
            return "continue"

        if policy_result == "watch":
            return "log"

        if policy_result == "realign":
            return "trigger_realign"

        if policy_result == "critical":
            return "halt_and_audit"
          
