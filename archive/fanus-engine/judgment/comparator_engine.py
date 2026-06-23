from typing import Dict


class ComparatorEngine:

    def __init__(self):

        # وزن‌ها برای تصمیم کیفیت
        self.weights = {
            "stability_gain": 0.35,
            "drift_reduction": 0.35,
            "trust_gain": 0.20,
            "noise_penalty": 0.10
        }

        self.last_score = 0.0

    # ─────────────────────────────
    # MAIN COMPARISON FUNCTION
    # ─────────────────────────────
    def evaluate(self, current: Dict, previous: Dict) -> Dict:

        # ─────────────────────────────
        # 1. EXTRACT SIGNALS
        # ─────────────────────────────
        current_drift = float(current.get("drift", 0.0))
        prev_drift = float(previous.get("drift", 0.0))

        current_trust = float(current.get("trust", {}).get("trust_score", 0.5))
        prev_trust = float(previous.get("trust", {}).get("trust_score", 0.5))

        current_stability = 1.0 - current_drift
        prev_stability = 1.0 - prev_drift

        # ─────────────────────────────
        # 2. DELTAS
        # ─────────────────────────────
        stability_gain = current_stability - prev_stability
        drift_reduction = prev_drift - current_drift
        trust_gain = current_trust - prev_trust

        noise_penalty = abs(stability_gain + trust_gain - drift_reduction) * 0.2

        # ─────────────────────────────
        # 3. FINAL QUALITY SCORE
        # ─────────────────────────────
        score = (
            stability_gain * self.weights["stability_gain"] +
            drift_reduction * self.weights["drift_reduction"] +
            trust_gain * self.weights["trust_gain"] -
            noise_penalty * self.weights["noise_penalty"]
        )

        # ─────────────────────────────
        # 4. DECISION
        # ─────────────────────────────
        is_better = score > 0.05

        # ─────────────────────────────
        # 5. UPDATE MEMORY
        # ─────────────────────────────
        if is_better:
            self.last_score = score

        return {
            "score": round(score, 4),
            "is_better": is_better,
            "trend": "improving" if is_better else "stable_or_worse",
            "delta": {
                "stability_gain": stability_gain,
                "drift_reduction": drift_reduction,
                "trust_gain": trust_gain,
                "noise_penalty": noise_penalty
            }
        }
