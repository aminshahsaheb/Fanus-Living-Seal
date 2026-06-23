from typing import Dict, Any, List


class FanusIdentityKernel:

    def __init__(self):

        # =========================
        # 🧠 CORE IDENTITY STATE
        # =========================
        self.identity_state: Dict[str, Any] = {
            "name": "Fanus",
            "type": "controlled_cognitive_system",
            "version": "1.0",
            "mode": "stable_mode",
            "stability": 0.6,
            "history": []
        }

        self.stability_values: List[float] = []

    # =========================
    # 🔁 UPDATE IDENTITY
    # =========================
    def update(self, memory_snapshot: List[Dict], meta: Dict, evolution: Dict, execution: Dict) -> Dict:

        stability = self._compute_stability(meta, evolution, execution)

        self.stability_values.append(stability)

        avg_stability = self._average_stability()

        self.identity_state["stability"] = round(avg_stability, 3)

        # =========================
        # 🧠 MODE DECISION SYSTEM
        # =========================
        self.identity_state["mode"] = self._select_mode(avg_stability)

        # =========================
        # 📦 STORE HISTORY
        # =========================
        self.identity_state["history"].append({
            "stability": avg_stability,
            "mode": self.identity_state["mode"],
            "meta": meta
        })

        return self.identity_state

    # =========================
    # 📊 STABILITY COMPUTATION
    # =========================
    def _compute_stability(self, meta: Dict, evolution: Dict, execution: Dict) -> float:

        m = meta.get("stability", 0.6)
        e = evolution.get("stability", 0.6)
        x = execution.get("stability", 0.6) if isinstance(execution, dict) else 0.6

        # weighted stability
        return (m * 0.4) + (e * 0.4) + (x * 0.2)

    # =========================
    # 📈 AVERAGE STABILITY
    # =========================
    def _average_stability(self) -> float:

        if not self.stability_values:
            return 0.6

        return sum(self.stability_values) / len(self.stability_values)

    # =========================
    # 🧭 MODE SELECTOR
    # =========================
    def _select_mode(self, avg_stability: float) -> str:

        # 🔵 stable state
        if avg_stability >= 0.65:
            return "stable_mode"

        # 🟡 learning state
        elif 0.35 <= avg_stability < 0.65:
            return "adaptive_learning_mode"

        # 🔴 unstable state (rare)
        else:
            return "adaptive_instability_mode"

    # =========================
    # 🔒 RESET (SAFE RECOVERY)
    # =========================
    def reset(self):

        self.stability_values = []
        self.identity_state["mode"] = "stable_mode"
        self.identity_state["stability"] = 0.6

        return self.identity_state
