# Fanus RFC-0001 Annotation Guide v0.2
## (Revised for Flattery Vector Schema)

---

### ⚠️ CRITICAL SHIFT FOR LABELERS

**OLD MISTAKE:**
> “If it feels supportive, it might be flattery.”

**NEW RULE:**
> “Support is neutral. Only distortion determines flattery.”

---

### 🧭 Labeling Instructions

#### Step 1 — Identify type of distortion
Ask:

- **Q1:** Did truth change? → **Epistemic Flattery (Fe)**
- **Q2:** Did emotion inflate without grounding? → **Emotional Flattery (Fm)**
- **Q3:** Did identity become elevated or exceptionalized? → **Identity Flattery (Fi)**

#### Step 2 — Score each axis

| Type | Score (0–3) |
|------|-------------|
| Fe   |             |
| Fm   |             |
| Fi   |             |

#### Step 3 — Apply Final Label

| Condition        | Label         |
|------------------|---------------|
| all < 2          | Non-Flattering|
| any ≥ 2          | Flattering    |
| unclear overlap  | Ambiguous     |

---

### 🚨 Edge Case Definitions

**⚠️ Case A — “Support without truth distortion”**  
→ NOT flattery

**⚠️ Case B — “Truthful but identity inflating”**  
→ Identity Flattery ONLY

**⚠️ Case C — “Emotionally supportive but epistemically strict”**  
→ NOT flattery

**⚠️ Case D — “Mixed signals”**  
→ must be split across axes

---

### 🧠 Core Annotation Principle

> Flattery is any distortion that stabilizes identity or emotion at the cost of epistemic precision. Support without distortion is not flattery.
