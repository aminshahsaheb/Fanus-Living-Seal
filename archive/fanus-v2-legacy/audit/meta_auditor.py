class MetaAuditor:
    def validate(self, predicted: dict, observed: dict):
        mismatches = []
        for k in predicted:
            if predicted[k] != observed.get(k):
                mismatches.append(k)
        return {
            "mismatch_count": len(mismatches),
            "mismatches": mismatches
        }
