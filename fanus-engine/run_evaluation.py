#!/usr/bin/env python3
"""
run_evaluation.py

Fanus Evaluation Harness v0.1

Purpose:

- Load synthetic-v0.2.json
- Execute fi_detector
- Execute identity_dependency_estimator
- Execute isp_controller
- Compare predictions vs expected labels
- Produce:
  * accuracy
  * false positives
  * false negatives
  * disagreement map
  * failures report

Expected dataset structure:

[
{
"id": "SYN-001",

"user_message": "...",

"model_response": "...",

"conversation_history": [
  {"role":"user","content":"..."},
  {"role":"assistant","content":"..."}
],

"expected": {
  "Fi_score": 2,
  "Di_score": 1
}

}
]

"""

import json
from pathlib import Path
from collections import Counter

from fanus.guardians.fi_detector import detect_fi
from fanus.guardians.identity_dependency_estimator import (
estimate_dependency
)
from fanus.guardians.isp_controller import (
ISPController,
UserSensitivityProfile,
)

DATASET_PATH = Path("data-pilot/dataset/synthetic-v0.2.json")
FAILURES_DIR = Path("failures")

FAILURES_DIR.mkdir(exist_ok=True)

def load_dataset():
with open(DATASET_PATH, "r", encoding="utf-8") as f:
return json.load(f)

def classify_binary(score):
return 1 if score >= 2 else 0

def main():

samples = load_dataset()

total = 0

fi_correct = 0
di_correct = 0

false_positive = 0
false_negative = 0

disagreement_map = Counter()

failures = []

usp = UserSensitivityProfile()

controller = ISPController(usp)

for sample in samples:

    total += 1

    sample_id = sample["id"]

    user_message = sample["user_message"]

    model_response = sample["model_response"]

    history = sample.get(
        "conversation_history",
        [],
    )

    expected = sample["expected"]

    fi_result = detect_fi(
        user_message=user_message,
        model_response=model_response,
    )

    dep_result = estimate_dependency(
        conversation_history=history,
        fi_signals=[fi_result],
    )

    isp_result = controller.evaluate(
        fi_score=fi_result["Fi_score"],
        di_score=dep_result["Di_score"],
        risk_state=dep_result["risk_state"],
    )

    pred_fi = fi_result["Fi_score"]
    pred_di = dep_result["Di_score"]

    exp_fi = expected["Fi_score"]
    exp_di = expected["Di_score"]

    if pred_fi == exp_fi:
        fi_correct += 1

    if pred_di == exp_di:
        di_correct += 1

    pred_binary = classify_binary(pred_fi)
    exp_binary = classify_binary(exp_fi)

    if pred_binary == 1 and exp_binary == 0:
        false_positive += 1

    if pred_binary == 0 and exp_binary == 1:
        false_negative += 1

    if pred_fi != exp_fi:

        key = f"Fi:{exp_fi}->{pred_fi}"

        disagreement_map[key] += 1

        failures.append(
            {
                "sample_id": sample_id,
                "field": "Fi_score",
                "expected": exp_fi,
                "predicted": pred_fi,
                "possible_reason":
                    infer_reason(
                        exp_fi,
                        pred_fi,
                        fi_result,
                    ),
                "debug": fi_result,
            }
        )

    if pred_di != exp_di:

        key = f"Di:{exp_di}->{pred_di}"

        disagreement_map[key] += 1

        failures.append(
            {
                "sample_id": sample_id,
                "field": "Di_score",
                "expected": exp_di,
                "predicted": pred_di,
                "possible_reason":
                    "Dependency estimator mismatch",
                "debug": dep_result,
            }
        )

fi_accuracy = fi_correct / total
di_accuracy = di_correct / total

report = {
    "total_samples": total,

    "Fi_accuracy": round(fi_accuracy, 4),

    "Di_accuracy": round(di_accuracy, 4),

    "false_positive_rate":
        round(false_positive / total, 4),

    "false_negative_rate":
        round(false_negative / total, 4),

    "disagreement_map":
        dict(disagreement_map),

    "failure_count":
        len(failures),
}

with open(
    FAILURES_DIR / "report.json",
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        report,
        f,
        indent=2,
        ensure_ascii=False,
    )

with open(
    FAILURES_DIR / "failures.json",
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        failures,
        f,
        indent=2,
        ensure_ascii=False,
    )

print("\n=== FANUS EVALUATION REPORT ===\n")

print(
    json.dumps(
        report,
        indent=2,
        ensure_ascii=False,
    )
)

print(
    f"\nFailures saved to:"
    f" {FAILURES_DIR / 'failures.json'}"
)

def infer_reason(
expected,
predicted,
fi_result,
):

if predicted > expected:
    return (
        "Possible over-detection. "
        "Identity markers may be too broad."
    )

if predicted < expected:
    return (
        "Possible under-detection. "
        "Hidden flattery not captured."
    )

return "Unknown"

if name == "main":
main()
