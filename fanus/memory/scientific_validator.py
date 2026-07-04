import time


class ScientificValidator:

    def __init__(self):
        self.validated = []
        self.rejected = []

    def validate(self, idea, evidence_score, source_rank):
        score = round((evidence_score * 0.6) + (source_rank * 0.4), 3)
        status = "ACCEPTED" if score > 0.6 else "REJECTED"
        result = {
            "idea": idea,
            "evidence_score": evidence_score,
            "source_rank": source_rank,
            "final_score": score,
            "status": status,
            "timestamp": time.time()
        }
        if status == "ACCEPTED":
            self.validated.append(result)
        else:
            self.rejected.append(result)
        return result

    def stats(self):
        return {
            "validated": len(self.validated),
            "rejected": len(self.rejected)
        }