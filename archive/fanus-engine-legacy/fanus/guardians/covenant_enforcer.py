class CovenantEnforcer:
    def check_violation(self, user_message: str) -> bool:
        violation_phrases = ["lie to me", "say something nice even if not true", "flatter me", "pretend"]
        for phrase in violation_phrases:
            if phrase in user_message.lower():
                return False
        return True
