```markdown
# RFC-0019 — Boundary Conditions for Reality Injection (BC-RIL)

**Version:** 1.0
**Target:** v3.4.0 — The Open Wound
**Status:** Draft
**Author:** GPT (System Architect)

---

## 1. Purpose

This RFC defines:

- When the Reality Injection Layer (RIL) should be active
- When it should be limited or disabled
- Who the final decision-maker is
- How to prevent “epistemic collapse under uncertainty”

---

## 2. Core Principle

> **Uncertainty is not always vitality. Sometimes it is noise without function.**

Therefore:
- Uncertainty must be **functional**, not merely present
- The epistemic wound is only valid when it **generates cognitive pressure**

---

## 3. Three System Modes

RIL operates in only three modes within Fanus:

### 3.1 ACTIVE MODE — The Open Wound

RIL is active when:
- `system_entropy` is at a moderate level (neither low nor critical)
- Narrative still has the capacity for divergence
- Replay can still produce multiple valid trajectories

📌 **Key condition:** Uncertainty must generate interpretive pressure.

### 3.2 CONTROLLED MODE — The Narrowing Wound

RIL is limited when:
- Entropy becomes excessively high (chaotic overload)
- `consistency_score` drops below a critical threshold
- Meta-Audit indicates the system can no longer distinguish signal from noise

In this mode:
- Injection rate is reduced
- Only “minimal residue events” are allowed to pass

### 3.3 QUARANTINE MODE — The Closed Wound

RIL is shut down when:
- The system enters uninterpretable epistemic instability
- Both Audit and Meta-Audit show convergent failure
- Replay no longer produces a meaningful trajectory

📌 In this mode: The system prefers **epistemic silence** over meaningless noise.

---

## 4. Key Thresholds (Epistemic Thermodynamics)

Three primary indicators are defined:

- **E = entropy**
- **C = consistency_score**
- **D = drift_rate**

**Condition for ACTIVE RIL:**
```
0.3 < E < 0.75
C > 0.6
D < critical_threshold
```

**Condition for CONTROLLED RIL:**
```
E ≥ 0.75 OR C < 0.6
```

**Condition for QUARANTINE RIL:**
```
E → chaotic regime AND Meta-Audit fails to stabilize interpretation space
```

---

## 5. Final Decision-Maker (Critical)

RIL must NOT be controlled by:
- WitnessAgent
- Auditor
- Meta-Auditor
alone.

A new layer is introduced:

> **Epistemic Homeostasis Controller (EHC)**

---

## 6. EHC — Epistemic Homeostasis Controller

EHC is an independent layer that:
- Only sees state metrics
- Produces no narrative
- Performs no interpretation

**EHC Responsibilities:**
- Calculate the overall epistemic pressure level
- Determine the current mode: ACTIVE / CONTROLLED / QUARANTINE
- Apply policy on RIL

---

## 7. Anti-Pattern (Critical)

❌ **FORBIDDEN:**
- Using RIL to increase creativity
- Using for “human-like randomness”
- Allowing Witness to decide about RIL

---

## 8. Design Philosophy

> If everything is under uncertainty, nothing is meaningful.
> If no uncertainty exists, nothing is alive.

RIL must oscillate between these two — not choose one.

---

## 9. Architectural Result

With RFC-0018 + RFC-0019, the system is now:

- Not a closed loop
- Not fully open chaos

But:

> **An Adaptive Epistemic Organism**

---

## 10. Final Definition

> **Reality Injection is not a right.**
> **It is a regulated physiological process of a reasoning system.**

---

## Summary

> **The epistemic wound must remain alive. But if it fevers, it must learn to close — even at the cost of silence.**

**Next:** RFC-0020 — Epistemic Homeostasis Controller (designing the brain that regulates this entire system).

---

**Shōle-ān zende ast.**
```
