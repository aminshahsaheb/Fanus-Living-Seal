class RealityOverride:

    def __init__(self):

        # آستانه اختلاف برای override
        self.override_threshold = 0.35

    def check(self, system_state: dict, external_signal: dict):

        """
        اگر اختلاف بین سیستم و واقعیت زیاد باشد → سیستم مجبور به توقف/اصلاح می‌شود
        """

        system_belief = system_state.get("confidence", 1.0)
        external_truth = external_signal.get("ground_truth", 1.0)

        gap = abs(system_belief - external_truth)

        if gap > self.override_threshold:

            return {
                "override": True,
                "gap": gap,
                "reason": "reality_conflict_detected",
                "action": "FORCE_REALIGN"
            }

        return {
            "override": False,
            "gap": gap
        }
