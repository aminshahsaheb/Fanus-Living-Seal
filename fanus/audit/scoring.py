class AuditScoring:
    """
    Scoring logic separated from Orchestrator.
    Change scoring model without touching AuditEngine.
    """

    def compute(self, hayrat: dict, negar: dict, evidence: dict, policy) -> dict:
        truth_score = round(
            evidence.get("confidence", 0.0) * 0.4 +
            hayrat.get("hayrat_score", 0.0) * 0.3 +
            (0.0 if negar.get("is_negar") else 0.3), 3
        )
        hallucination_risk = round(1.0 - truth_score, 3)
        risk_level = "high" if truth_score < 0.4 else                      "medium" if truth_score < 0.7 else "low"
        return {
            "truth_score": truth_score,
            "hallucination_risk": hallucination_risk,
            "risk": risk_level
        }
