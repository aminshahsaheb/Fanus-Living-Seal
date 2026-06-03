# fanus-engine/learning/self_tuner.py

class SelfTuner:

    def __init__(self, parameter_store, wound_ledger):
        self.params = parameter_store
        self.wounds = wound_ledger

    def analyze_and_update(self):

        data = self.wounds.load()

        if len(data) == 0:
            return

        drift_errors = [
            w for w in data
            if w["type"] == "DRIFT_SPIKE"
        ]

        if len(drift_errors) == 0:
            return

        avg_severity = sum(w["severity"] for w in drift_errors) / len(drift_errors)

        # ─────────────────────────────
        # SELF CORRECTION RULES
        # ─────────────────────────────

        if avg_severity > 0.7:
            # system too unstable → increase alignment weight
            self.params.update_weight("alignment",
                                       self.params.weights["alignment"] + 0.05)

        elif avg_severity < 0.4:
            # system too conservative → allow more narrative
            self.params.update_weight("narrative",
                                       self.params.weights["narrative"] + 0.03)
