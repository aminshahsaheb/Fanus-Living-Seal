class PolicyValidator:

    def __init__(self):

        # حداقل اطمینان برای اعمال تغییر
        self.min_confidence = 0.65

        # حداقل تکرار scar
        self.min_occurrence = 3

    def validate(self, scars: dict, current_policy: dict):

        """
        بررسی می‌کند آیا اجازه داریم policy را تغییر بدهیم یا نه
        """

        if not scars:
            return {
                "allowed": False,
                "reason": "no_scars_available"
            }

        decisions = []

        for scar_type, scar_data in scars.items():

            count = scar_data.get("count", 0)
            severity = scar_data.get("severity_avg", 0.0)

            # confidence مصنوعی از ترکیب شدت و تکرار
            confidence = min(1.0, (count * 0.2) + severity)

            if count < self.min_occurrence:
                decisions.append((scar_type, False, "insufficient_occurrence"))
                continue

            if confidence < self.min_confidence:
                decisions.append((scar_type, False, "low_confidence"))
                continue

            decisions.append((scar_type, True, "approved"))

        allowed = any(d[1] for d in decisions)

        return {
            "allowed": allowed,
            "decisions": decisions
        }
