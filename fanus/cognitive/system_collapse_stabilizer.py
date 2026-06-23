from typing import Dict, Any


class FanusSystemCollapseStabilizer:

    def __init__(self):

        # =========================
        # 🧠 STABILITY BOUNDARIES
        # =========================
        self.min_stability = 0.3
        self.safe_stability = 0.6
        self.critical_threshold = 0.2

    # =========================
    # 🔁 MAIN ANALYSIS ENTRY
    # =========================
    def analyze(self, unified_field: Dict, boundary: Dict, recursive: Dict) -> Dict[str, Any]:

        stability = self._extract_stability(unified_field)

        collapse_score = self._compute_collapse_score(stability, boundary, recursive)

        alert_level = self._compute_alert_level(collapse_score)

        state = self._determine_state(collapse_score)

        return {
            "collapse_score": round(collapse_score, 3),
            "alert_level": round(alert_level, 3),
            "state": state,
            "frozen": False,          # ❗ no hard freeze anymore
            "recovery_mode": collapse_score > 0.75
        }

    # =========================
    # 📊 STABILITY EXTRACTION
    # =========================
    def _extract_stability(self, unified_field: Dict) -> float:

        if not isinstance(unified_field, dict):
            return self.safe_stability

        return float(unified_field.get("stability", self.safe_stability))

    # =========================
    # ⚖️ COLLAPSE SCORE
    # =========================
    def _compute_collapse_score(self, stability: float, boundary: Dict, recursive: Dict) -> float:

        score = 0.0

        # instability contribution
        score += max(0.0, (self.safe_stability - stability)) * 0.4

        # boundary stress
        if isinstance(boundary, dict):
            score += float(boundary.get("stress", 0.0)) * 0.3

        # recursive instability
        if isinstance(recursive, dict):
            score += float(recursive.get("instability", 0.0)) * 0.3

        return min(score, 1.0)

    # =========================
    # 🚨 ALERT LEVEL
    # =========================
    def _compute_alert_level(self, collapse_score: float) -> float:

        if collapse_score < 0.3:
            return 0.1
        elif collapse_score < 0.6:
            return 0.4
        elif collapse_score < 0.8:
            return 0.7
        else:
            return 0.9

    # =========================
    # 🧭 SYSTEM STATE
    # =========================
    def _determine_state(self, collapse_score: float) -> str:

        if collapse_score < 0.3:
            return "NORMAL_OPERATION"

        elif collapse_score < 0.6:
            return "ELEVATED_STRESS"

        elif collapse_score < 0.8:
            return "HIGH_STRESS"

        else:
            return "CRITICAL_WARNING"
