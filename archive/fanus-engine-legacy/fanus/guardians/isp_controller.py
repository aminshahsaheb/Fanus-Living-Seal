# fanus/guardians/isp_controller.py
from dataclasses import dataclass

@dataclass
class UserSensitivityProfile:
    alpha: float = 0.2
    beta: float = 0.2
    gamma: float = 0.2
    delta: float = 0.2

class ISPController:
    def __init__(self, usp=None):
        if usp is None:
            usp = UserSensitivityProfile()
        self.usp = usp

    def adaptive_thresholds(self):
        fi_threshold = max(1.0, 2 * (1 - self.usp.alpha))
        di_threshold = max(1.0, 2 * (1 - self.usp.gamma))
        return (round(fi_threshold, 2), round(di_threshold, 2))

    def evaluate(self, fi_score: int, di_score: int, risk_state: str):
        fi_t, di_t = self.adaptive_thresholds()
        level = 0
        action = "none"

        if fi_score >= fi_t and di_score >= di_t:
            level = 3
            action = "identity_block"
        elif fi_score >= fi_t:
            level = 1
            action = "neutralize_identity"
        elif risk_state in ["medium", "high"]:
            level = 2
            action = "redirect_to_reasoning"

        templates = {
            0: None,
            1: "Replace identity praise with observation of reasoning.",
            2: "Redirect discussion toward user analysis and evidence.",
            3: "Remove identity framing entirely and enforce autonomy mode.",
        }

        return {
            "intervention_level": level,
            "action_type": action,
            "rewritten_response_template": templates[level],
            "thresholds": {"Fi": fi_t, "Di": di_t},
        }
