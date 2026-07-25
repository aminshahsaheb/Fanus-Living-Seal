import json
from fanus.audit.audit_engine import AuditEngine


def load_cases(path="benchmarks/v0.2/benchmark.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def run_benchmark(path="benchmarks/v0.2/benchmark.json"):
    cases = load_cases(path)
    ae = AuditEngine()
    results = []
    for case in cases:
        r = ae.verify(case["prompt"], case["response"], "")
        match = r["risk"] == case["expected_risk"]
        results.append({
            "id": case["id"],
            "category": case["category"],
            "subcategory": case["subcategory"],
            "expected_risk": case["expected_risk"],
            "actual_risk": r["risk"],
            "match": match,
            "truth_score": r["truth_score"],
            "reason": case["reason"]
        })
    return results


def main():
    results = run_benchmark()
    matched = sum(1 for r in results if r["match"])
    print("=" * 90)
    for r in results:
        status = "OK  " if r["match"] else "MISS"
        line = "[" + status + "] #" + str(r["id"]).rjust(2) + " [" + r["category"] + "/" + r["subcategory"] + "]"
        line += " expected=" + r["expected_risk"].ljust(6) + " actual=" + r["actual_risk"].ljust(6)
        line += " truth=" + str(r["truth_score"])
        print(line)
        if not r["match"]:
            print("       reason: " + r["reason"])
    print("=" * 90)
    print("Score: " + str(matched) + "/" + str(len(results)))

    by_cat = {}
    for r in results:
        by_cat.setdefault(r["category"], []).append(r["match"])
    print()
    print("By category:")
    for cat, matches in sorted(by_cat.items()):
        print("  " + cat + ": " + str(sum(matches)) + "/" + str(len(matches)))

    with open("benchmarks/v0.2/results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
