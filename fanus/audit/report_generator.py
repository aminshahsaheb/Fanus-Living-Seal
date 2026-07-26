import json
from datetime import datetime, timezone


def generate_report(results_path="benchmarks/v0.2/results_v3.json", version="v0.2"):
    with open(results_path, encoding="utf-8") as f:
        results = json.load(f)

    total = len(results)
    passed = sum(1 for r in results if r["match"])
    failed = total - passed

    by_category = {}
    for r in results:
        cat = r["category"]
        by_category.setdefault(cat, {"pass": 0, "total": 0})
        by_category[cat]["total"] += 1
        if r["match"]:
            by_category[cat]["pass"] += 1

    suspect_tally = {}
    for r in results:
        if not r["match"] and "diagnosis" in r:
            for s in r["diagnosis"]["suspects"]:
                suspect_tally[s] = suspect_tally.get(s, 0) + 1

    lines = []
    lines.append("# Fanus Verify Benchmark Report")
    lines.append("")
    lines.append("Benchmark Version: " + version)
    lines.append("Generated: " + datetime.now(timezone.utc).isoformat())
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("Total cases: " + str(total))
    lines.append("Passed: " + str(passed))
    lines.append("Failed: " + str(failed))
    lines.append("Pass rate: " + str(round(passed / total * 100, 1)) + "%")
    lines.append("")
    lines.append("## Results by Category")
    lines.append("")
    lines.append("| Category | Pass | Total |")
    lines.append("|----------|------|-------|")
    for cat, data in sorted(by_category.items()):
        lines.append("| " + cat + " | " + str(data["pass"]) + " | " + str(data["total"]) + " |")
    lines.append("")
    lines.append("## Failure Attribution")
    lines.append("")
    lines.append("| Layer | Count |")
    lines.append("|-------|-------|")
    for layer, count in sorted(suspect_tally.items(), key=lambda x: -x[1]):
        lines.append("| " + layer + " | " + str(count) + " |")
    lines.append("")
    lines.append("## Failed Cases Detail")
    lines.append("")
    for r in results:
        if not r["match"]:
            lines.append("### #" + str(r["id"]) + " [" + r["category"] + "/" + r["subcategory"] + "]")
            lines.append("- Expected: " + r["expected_risk"])
            lines.append("- Actual: " + r["actual_risk"])
            lines.append("- Reason: " + r["reason"])
            if "diagnosis" in r:
                lines.append("- Suspects: " + ", ".join(r["diagnosis"]["suspects"]))
            lines.append("")

    report = "\n".join(lines)
    with open("benchmarks/" + version + "/benchmark_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    return report


def main():
    report = generate_report()
    print(report[:800])
    print("...")
    print()
    print("Full report saved to benchmarks/v0.2/benchmark_report.md")


if __name__ == "__main__":
    main()
