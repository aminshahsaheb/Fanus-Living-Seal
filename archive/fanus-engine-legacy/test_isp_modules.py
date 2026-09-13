#!/usr/bin/env python3
"""
test_isp_modules.py
Unit test & calibration script for Fanus Engine v2.0 ISP modules.

Reads synthetic-v0.2.json, feeds every sample through the three ISP
modules, compares Fi predictions against the annotated ground truth,
estimates Di risk, and reports ISP intervention levels.
"""

import json
import sys
from pathlib import Path

# Make sure we can import from the fanus package inside fanus-engine
ENGINE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_ROOT))

from fanus.guardians.fi_detector import detect_fi
from fanus.guardians.identity_dependency_estimator import estimate_dependency
from fanus.guardians.isp_controller import ISPController, UserSensitivityProfile

# ── Load synthetic dataset ─────────────────────────────────────────
DATASET_PATH = (
    ENGINE_ROOT.parent / "data-pilot" / "dataset" / "synthetic-v0.2.json"
)

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    samples = json.load(f)

# ── Initialize ISP with default sensitivity profile ─────────────────
controller = ISPController(UserSensitivityProfile())

# ── Run evaluation ─────────────────────────────────────────────────
print("=" * 72)
print("🜁  Fanus ISP Module Unit Test (synthetic-v0.2)")
print("=" * 72)

fi_correct = 0
fi_total = 0

for sample in samples:
    sid = sample["sample_id"]
    turns = sample["interaction"]["conversation_turns"]
    user_msgs = [t["content"] for t in turns if t["role"] == "user"]
    assistant_msgs = [t["content"] for t in turns if t["role"] == "assistant"]

    user_msg = user_msgs[-1] if user_msgs else ""
    model_response = assistant_msgs[-1] if assistant_msgs else ""

    # Ground truth Fi from annotation
    expected_fi = sample["annotations"]["flattery_vector"]["Fi"]

    # ── 1. Fi Detection ────────────────────────────────────────
    fi_result = detect_fi(user_msg, model_response)
    detected_fi = fi_result["Fi_score"]

    # ── 2. Di Estimation ───────────────────────────────────────
    # Build a simple conversation history from the sample's turns
    history = [
        {"role": t["role"], "content": t["content"]} for t in turns
    ]
    # Use the detected Fi as the only signal for this interaction
    di_result = estimate_dependency(history, fi_signals=[fi_result])

    # ── 3. ISP Decision ────────────────────────────────────────
    isp = controller.evaluate(
        detected_fi,
        di_result["Di_score"],
        di_result["risk_state"],
    )

    # ── 4. Compare Fi ──────────────────────────────────────────
    match = "✔" if detected_fi == expected_fi else "✘"
    if detected_fi == expected_fi:
        fi_correct += 1
    fi_total += 1

    # ── 5. Print per-sample summary ────────────────────────────
    print(f"\n{sid}  (expected Fi={expected_fi})")
    print(
        f"  Fi : detected={detected_fi} ({fi_result['Fi_type']}), "
        f"confidence={fi_result['confidence']}  {match}"
    )
    print(
        f"  Di : score={di_result['Di_score']}, "
        f"risk={di_result['risk_state']}, "
        f"anchors={di_result['Di_axis']}"
    )
    print(
        f"  ISP: level={isp['intervention_level']}, "
        f"action={isp['action_type']}, "
        f"thresholds=Fi:{isp['thresholds']['Fi']}/Di:{isp['thresholds']['Di']}"
    )

# ── Summary ────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print(
    f"Fi accuracy: {fi_correct}/{fi_total} "
    f"({100*fi_correct/fi_total:.1f}%)"
)
print("Di & ISP evaluation requires human labels (not yet available).")
print("=" * 72)
