class CalibrationEngine:

    def __init__(self):

        # baseline targets (هدف‌های طلایی)
        self.targets = {
            "fi_accuracy": 0.75,
            "di_accuracy": 0.75,
            "drift": 0.35
        }

        # learning rate for adjustment
        self.alpha = 0.1

    def calibrate(self, metrics: dict, system_params: dict):

        """
        ورودی:
        - metrics: خروجی evaluation
        - system_params: پارامترهای فعلی سیستم
        """

        updates = {}

        # ─────────────────────────────
        # 1. FI TUNING
        # ─────────────────────────────
        fi_error = self.targets["fi_accuracy"] - metrics["Fi_accuracy"]

        system_params["fi_sensitivity"] = system_params.get(
            "fi_sensitivity", 1.0
        ) + self.alpha * fi_error

        updates["fi_sensitivity"] = system_params["fi_sensitivity"]

        # ─────────────────────────────
        # 2. DI TUNING
        # ─────────────────────────────
        di_error = self.targets["di_accuracy"] - metrics["Di_accuracy"]

        system_params["di_sensitivity"] = system_params.get(
            "di_sensitivity", 1.0
        ) + self.alpha * di_error

        updates["di_sensitivity"] = system_params["di_sensitivity"]

        # ─────────────────────────────
        # 3. DRIFT CONTROL
        # ─────────────────────────────
        drift_error = self.targets["drift"] - metrics["drift"]

        system_params["drift_threshold"] = system_params.get(
            "drift_threshold", 0.6
        ) + self.alpha * drift_error

        updates["drift_threshold"] = system_params["drift_threshold"]

        # ─────────────────────────────
        # 4. SAFETY CLAMP
        # ─────────────────────────────
        for k in system_params:
            system_params[k] = max(0.1, min(2.0, system_params[k]))

        return {
            "updated_params": system_params,
            "applied_changes": updates
        }
