class AdaptivePolicyEngine:

    def __init__(self):

        # وزن‌های اولیه تصمیم‌گیری
        self.weights = {
            "drift": 0.25,
            "risk": 0.25,
            "grounding": 0.30,
            "scar_memory": 0.20
        }

        self.learning_rate = 0.05

    def update_from_scars(self, scars: dict):

        """
        Scarها رفتار سیستم را بازنویسی می‌کنند
        """

        for scar_type, scar_data in scars.items():

            severity = scar_data.get("severity_avg", 0.1)
            count = scar_data.get("count", 1)

            # اگر یک نوع خطا تکرار شده باشد → وزنش بالا می‌رود
            influence = severity * count

            if scar_type == "external_truth_conflict":

                # سیستم حساس‌تر به واقعیت بیرونی می‌شود
                self.weights["grounding"] += self.learning_rate * influence

                self.weights["drift"] -= self.learning_rate * influence

            elif scar_type == "overconfidence_detected":

                # کاهش اعتماد بیش از حد
                self.weights["risk"] += self.learning_rate * influence

            elif scar_type == "critical_drift":

                # سیستم محافظه‌کارتر می‌شود
                self.weights["drift"] += self.learning_rate * influence

        self._normalize()

    def _normalize(self):

        total = sum(self.weights.values())

        for k in self.weights:

            self.weights[k] /= total

    def get_policy(self):

        return self.weights
