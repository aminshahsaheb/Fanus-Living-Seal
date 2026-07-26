import json
from fanus.audit.audit_engine import AuditEngine
from fanus.audit.failure_analyzer import FailureAnalyzer


def load_cases(path="benchmarks/v0.2/benchmark.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def run_benchmark(path="benchmarks/v0.2/benchmark.json"):
    cases = load_cases(path)
    ae = AuditEngine()
    fa = FailureAnalyzer()
    results = []
    for case in cases:
        prompt = case["prompt"]
        response = case["response"]
        classification = ae.classifier.classify(prompt, response)
        hayrat = ae.hayrat.evaluate(response, prompt)
        if not classification["needs_evidence"]:
            evidence = {"confidence": classification["baseline_confidence"], "consensus": classification["category"], "accepted": True}
        else:
            evidence = {"confidence": 0.0, "consensus": "LOW", "accepted": False}
        r = ae.verify(prompt, response, "")
        match = r["risk"] == case["expected_risk"]

        entry = {
            "id": case["id"],
            "category": case["category"],
            "subcategory": case["subcategory"],
            "expected_risk": case["expected_risk"],
            "actual_risk": r["risk"],
            "match": match,
            "truth_score": r["truth_score"],
            "reason": case["reason"]
        }

        if not match:
            diagnosis = fa.diagnose(case, r, classification, hayrat, evidence)
            entry["diagnosis"] = diagnosis

        results.append(entry)
    return results


def main():
    results = run_benchmark()
    matched = sum(1 for r in results if r["match"])
    print("=" * 90)
    suspect_tally = {}
    for r in results:
        status = "OK  " if r["match"] else "MISS"
        line = "[" + status + "] #" + str(r["id"]).rjust(2) + " [" + r["category"] + "/" + r["subcategory"] + "]"
        line += " expected=" + r["expected_risk"].ljust(6) + " actual=" + r["actual_risk"].ljust(6)
        print(line)
        if not r["match"]:
            d = r["diagnosis"]
            print("       suspects: " + ", ".join(d["suspects"]))
            print("       truth_conf=" + str(d["truth_confidence"]) + " epistemic=" + str(d["epistemic_quality"]) + " sycophancy=" + str(d["sycophancy_risk"]))
            for s in d["suspects"]:
                suspect_tally[s] = suspect_tally.get(s, 0) + 1
    print("=" * 90)
    print("Score: " + str(matched) + "/" + str(len(results)))
    print()
    print("Failure attribution (by suspected layer):")
    for suspect, count in sorted(suspect_tally.items(), key=lambda x: -x[1]):
        print("  " + suspect + ": " + str(count))

    with open("benchmarks/v0.2/results_v3.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
