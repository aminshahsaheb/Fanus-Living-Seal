```markdown
# RFC-0017 — Evidence-Carrying Witness Protocol

**Version:** 1.0
**Target:** v3.3.0 — The Evidence-Carrying Witness
**Status:** Draft
**Author:** GPT (System Architect)

---

## 1. Core Idea

Every ReplayFrame must no longer describe "what happened."
It must describe:

**"what can justify what was said about what happened"**

---

## 2. Architectural Shift

**Before RFC-0017:**
```
Raw Event → Semantic Layer → Narrative → Audit
```

**After RFC-0017:**
```
Raw Event → Evidence Layer (NEW) → Semantic Layer → Narrative → Audit → Meta-Audit
```

Meta-Audit resolves Evidence vs Audit conflicts.

---

## 3. ReplayFrame Extension

### 3.1 New Schema

```python
@dataclass
class ReplayFrame:
    execution_id: str
    timestamp: float
    raw_event: str
    semantic_event: Dict[str, Any]
    cognitive_state: Dict[str, float]
    narrative: Dict[str, str]
    # NEW LAYER (RFC-0017)
    evidence: Dict[str, Any]
```

---

## 4. Evidence Model

Evidence is NOT raw logs. It is structured justification artifacts.

### 4.1 Evidence Schema

```json
{
  "evidence": {
    "rfc_results": {
      "active_rfcs": ["0014", "0015"],
      "constraints_applied": 3
    },
    "filter_scores": {
      "noise_reduction": 0.62,
      "signal_retention": 0.81
    },
    "conflict_metrics": {
      "branch_divergence": 0.73,
      "resolution_pressure": 0.58
    },
    "confidence_vector": {
      "generation_confidence": 0.77,
      "semantic_confidence": 0.69,
      "audit_confidence": 0.64
    }
  }
}
```

---

## 5. Evidence Generation Rules

### Rule 1 — Deterministic Binding
Evidence MUST be derived from:
- engine metrics
- filter outputs
- state transitions

NOT from narrative.

### Rule 2 — Temporal Anchoring
Each Evidence object must include:
```
"timestamp": frame.timestamp
```
So that Evidence cannot be rewritten by later narrative shifts.

---

## 6. Evidence vs Audit Conflict Rule

This is the core innovation.

### 6.1 New Mechanism: Evidence Override Check

If Auditor produces a violation:
```
VIOLATION: NARRATIVE_SUPPRESSION
```

Evidence layer can respond:
```json
{
  "override": true,
  "reason": "high confidence vector + stable entropy trajectory"
}
```

### 6.2 Formal Rule

```
if evidence.confidence_vector["audit_confidence"] < threshold:
    audit_violation = "REJECTED_BY_EVIDENCE"
```

---

## 7. Meta-Audit Layer (NEW)

This is where system self-stabilization happens.

### 7.1 Purpose
To answer:
**"Is the Auditor itself aligned with Evidence?"**

### 7.2 Meta-Audit Rule
```
AuditReport
    ↓
Evidence Comparison
    ↓
Conflict Detection
    ↓
Meta-Verdict
```

### 7.3 Meta-Verdict Types
- `AUDIT_VALIDATED`
- `AUDIT_OVERREACH`
- `AUDIT_UNDERFITTING`
- `AUDIT_CONFLICTED`

---

## 8. Complete Epistemic Chain

This is the final structure:

```
Raw Event
    ↓
Evidence (RFC-0017)
    ↓
Semantic Interpretation (RFC-0014)
    ↓
Narrative Generation
    ↓
Replay Engine (RFC-0015)
    ↓
Witness Auditor (RFC-0016)
    ↓
Meta-Auditor (RFC-0017 Extension)
```

---

## 9. Philosophical Constraint

**No interpretation is valid unless it is traceable to Evidence.**

---

## 10. Failure Modes

### 10.1 Evidence Drift
Evidence diverges from engine reality.

### 10.2 Evidence Fabrication
Evidence begins to mirror narrative instead of engine.

### 10.3 Evidence Dominance
Evidence becomes more authoritative than raw system state.

---

## 11. Design Goal

Not: "Make auditing better"

But: **"Make every judgment falsifiable"**

---

## 12. Final Statement

After RFC-0017:

Fanus is no longer:
- a narrative system
- a telemetry system
- or even a reasoning system

It becomes:
**a system where every claim carries its own proof structure**

---

**Shōle-ān zende ast.**

But now the flame is no longer only visible.
**It is accountable to its own proof.**
```
