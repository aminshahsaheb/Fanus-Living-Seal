class MetaAuditor:

    def audit(self, report):

        warnings = []

        drift = report["drift"]

        confidence = report["state"].get(
            "confidence",
            1.0
        )

        grounding = report["grounding"]

        if confidence > 0.9 and drift > 0.5:

            warnings.append(
                "overconfidence_detected"
            )

        if grounding["mismatch"]:

            warnings.append(
                "external_reality_conflict"
            )

        if drift > 0.8:

            warnings.append(
                "critical_drift"
            )

        if len(warnings) == 0:

            status = "HEALTHY"

        elif len(warnings) < 3:

            status = "WARNING"

        else:

            status = "CRITICAL"

        return {
            "status": status,
            "warnings": warnings
        }
