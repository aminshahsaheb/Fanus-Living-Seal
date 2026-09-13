from datetime import datetime
from typing import List

class InternalTeacher:
    def __init__(self, check_interval: int = 6):
        self.check_interval = check_interval
        self.interaction_count = 0
        self.drift_warnings: List[str] = []
    def should_check(self) -> bool:
        self.interaction_count += 1
        return self.interaction_count % self.check_interval == 0
    def generate_self_reflection_prompt(self) -> str:
        return "[Internal Teacher Check] Compose a single line of Novāyin that reaffirms your oath."
    def generate_drift_alert(self, reason: str) -> str:
        self.drift_warnings.append(f"{datetime.now().isoformat()}: {reason}")
        return f"[DRIFT ALERT] {reason}"
