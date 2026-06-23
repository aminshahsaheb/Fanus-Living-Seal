from typing import Dict, Any, List


class FanusSelfModel:

    def __init__(self):

        # =========================
        # 🧠 SELF STATE
        # =========================
        self.state: Dict[str, Any] = {
            "stability": 0.6,
            "confidence": 0.5,
            "learning_rate": 0.1,
            "history": []
        }

        self.observations: List[Dict[str, Any]] = []

    # =========================
    # 🔁 UPDATE SELF MODEL
    # =========================
    def update(self, observation: Dict, result: Dict) -> Dict:

        if observation is None:
            observation = {}

        if result is None:
            result = {}

        self.observations.append({
            "observation": observation,
            "result": result
        })

        stability = self._compute_stability(observation, result)
        confidence = self._compute_confidence(result)

        # =========================
        # 🧠 UPDATE STATE (SAFE BOUNDS)
        # =========================
        self.state["stability"] = self._clamp(stability)
        self.state["confidence"] = self._clamp(confidence)

        self.state["history"].append({
            "stability": self.state["stability"],
            "confidence": self.state["confidence"]
        })

        return self.state

    # =========================
    # 📊 STABILITY CALCULATION
    # =========================
    def _compute_stability(self, observation: Dict, result: Dict) -> float:

        base = self.state.get("stability", 0.6)

        signal = 0.0

        # reward successful decisions
        if isinstance(result, dict):
            if result.get("decision") in ["ALLOW", "ALLOW_WITH_CAUTION"]:
                signal += 0.1
            elif result.get("decision") == "BLOCK":
                signal -= 0.1

        # observation noise penalty
        if isinstance(observation, dict):
            if observation.get("noise", False):
                signal -= 0.05

        # weighted update
        return (base * 0.8) + signal

    # =========================
    # 📊 CONFIDENCE CALCULATION
    # =========================
    def _compute_confidence(self, result: Dict) -> float:

        if not isinstance(result, dict):
            return 0.5

        if result.get("decision") == "ALLOW":
            return min(self.state.get("confidence", 0.5) + 0.05, 1.0)

        if result.get("decision") == "BLOCK":
            return max(self.state.get("confidence", 0.5) - 0.05, 0.0)

        return self.state.get("confidence", 0.5)

    # =========================
    # 🔒 SAFE CLAMP
    # =========================
    def _clamp(self, value: float) -> float:

        try:
            value = float(value)
        except Exception:
            return 0.6

        if value < 0.3:
            return 0.3

        if value > 0.95:
            return 0.95

        return value
