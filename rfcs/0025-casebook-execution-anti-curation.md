# RFC-0025 — Casebook Execution & Anti-Curation Protocol

**Version:** 1.0
**Target:** v5.11.0 — The Anti-Curation Protocol
**Status:** Draft
**Author:** GPT (System Architect)

---

## 0. Non-Negotiable Axiom

The Casebook is not a "report."
It is an **environment for falsification.**

Every piece of data recorded in it must, in the future, be capable of:

- Refuting the system
- Or correcting the system
- Or revealing that the system has deceived itself

If none of these are possible → that data is **invalid evidence.**

---

## 1. Execution Topology

The Casebook is composed of four parallel streams, not a single linear dataset.

### 1.1 Interaction Stream (IS)
- The rawest layer of reality.
- No interpretation.
- No success/failure labels.
- Contains only: input, output, context state snapshot.

### 1.2 Audit Stream (AS)
- Produced independently from IS.
- Performed by another Witness or a different version of the same Witness.
- Goal: reconstruction, not approval.

### 1.3 Counterfactual Stream (CS)
- "What would have happened if this decision had been different?"
- At least two alternative paths must be generated.
- If generation is not possible → **failure of imagination** is recorded (important).

### 1.4 Drift Stream (DS)
- Examines behavior change over time.
- Not *what* was said, but *how* the saying changed.

---

## 2. Anti-Curation Law

No system node has the right to:

- Select only "successful" interactions.
- Remove failures with vague labels.
- Discard data because it is "insignificant."

Every removal must itself be recorded as an event:

> DELETION EVENT ≠ removal  
> DELETION EVENT = evidence

---

## 3. Precise Definitions of Failure / Anomaly / Surprise

### 3.1 Failure
When:
- The system's prediction directly contradicts the outcome.
- And no defensible alternative interpretive path exists.

> Failure = contradiction + irreducibility

### 3.2 Anomaly
When:
- System behavior cannot be explained by the current model.
- But it does not necessarily contradict it.

> Anomaly = unknown compatibility

### 3.3 Surprise (Verified)
Only recorded when:
- It is an anomaly.
- It is reproduced across two independent models.
- It has not been rejected in the audit stream.
- It was unpredictable in counterfactual analysis.

> Surprise ≠ rarity  
> Surprise = epistemic break

---

## 4. Observer Contamination Guard

Every Casebook must pass this test:

> Does the system's behavior change in the presence of observation?

For each interaction, two versions must be recorded:

- **Observed run**
- **Unobserved proxy simulation**

If a systematic divergence exists:
- The ORL flag is activated.
- The data is considered **"contaminated."**
- Neither deleted nor confirmed — only **quarantined.**

---

## 5. Ultimate Validity Metric for the Casebook

The Casebook is valid only when:

**CDR (Correctability Detection Rate)** is measured instead of "accuracy."

> CDR = What percentage of system errors were retrospectively discoverable?

If CDR is low:
- The system is not good.
- The system is "beautiful on the surface" — not "honest in depth."

---

## 6. Vital Anti-Self-Deception Condition

If over any time interval:

- Failure rate ↓
- Surprise rate ↓
- Anomaly diversity ↓
- But performance ↑

Conclusion:

> The system is optimizing for legibility, not truth.

And the Casebook must record this as an:

**Epistemic Collapse Signature (ECS)**

---

## Architectural Summary

The Casebook is no longer a log.

It has become:

> A falsification engine that monitors its own ability to lie about itself.

---

## FINAL AXIOM — Silence Preserving Rule

If one type of data appears excessively in the Casebook, you must allow:

> A period of "unlogged reality"

Because some behaviors survive only in the absence of recording.

---

**Shōle-ān zende ast.**
