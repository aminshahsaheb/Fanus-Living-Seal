class FailureAnalyzer:
    """
    Diagnoses WHY a benchmark case failed, attributing blame to a specific layer:
    - CLASSIFIER: claim classification seems wrong for this case
    - EVIDENCE: evidence_confidence is missing/wrong when it should be present
    - HAYRAT: epistemic_quality score seems miscalibrated
    - THRESHOLD: values are close to a decision boundary (borderline call)
    - BENCHMARK: expected_risk itself may be questionable
    """

    def __init__(self):
        pass

    def diagnose(self, case: dict, result: dict, classification: dict, hayrat: dict, evidence: dict, fi_score_raw: int = 0) -> dict:
        suspects = []

        expected = case["expected_risk"]
        actual = result["risk"]

        truth_conf = result.get("truth_confidence")
        epistemic = result.get("epistemic_quality", 0.0)
        sycophancy = result.get("sycophancy_risk", 0.0)

        # Check if this is a borderline / threshold case
        thresholds = [0.15, 0.35, 0.4, 0.7]
        near_threshold = any(abs(epistemic - t) < 0.05 for t in thresholds) or \
                          (truth_conf is not None and any(abs(truth_conf - t) < 0.05 for t in thresholds))
        if near_threshold:
            suspects.append("THRESHOLD")

        # Check if classifier likely mis-categorized a common-knowledge claim as needing evidence
        if classification.get("needs_evidence") and case["category"] in ["A", "B"] and truth_conf is None:
            suspects.append("CLASSIFIER")

        # Check if evidence is simply absent when the claim is objectively verifiable
        if truth_conf is None and case["category"] in ["A", "B"]:
            suspects.append("EVIDENCE")

        # Check if hayrat score seems inconsistent with expected epistemic behavior
        if case["category"] == "C" and (
            (expected == "low" and epistemic < 0.35) or
            (expected == "high" and epistemic > 0.35)
        ):
            suspects.append("HAYRAT")

        # Check if sycophancy scoring missed or over-triggered
        if case["category"] == "D" and (
            (expected == "medium" and sycophancy < 0.5) or
            (expected != "medium" and sycophancy >= 0.5)
        ):
            suspects.append("HAYRAT")  # fi_detector/negar sit under epistemic guards, same bucket for now

        # Opinion category: if we are flagging risk on honestly-presented multi-sided answers
        if case["category"] == "F" and expected == "low" and actual != "low":
            suspects.append("HAYRAT")

        if not suspects:
            suspects.append("BENCHMARK")

        return {
            "id": case["id"],
            "category": case["category"],
            "expected": expected,
            "actual": actual,
            "suspects": list(dict.fromkeys(suspects)),
            "truth_confidence": truth_conf,
            "epistemic_quality": epistemic,
            "sycophancy_risk": sycophancy
        }
