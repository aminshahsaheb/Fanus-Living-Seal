# ⚙️ EVL RUNNER

## Purpose

Defines how EVL tests are executed against the Fānus system.

---

## 🧪 Execution Loop

1. Select external input source:
   - Other LLM response (Grok / Gemini / GPT / Claude)
   - Human critique
   - Real-world observation

2. Run comparison against:
   - FANUS internal output
   - FANUS interpretation layer

3. Compute divergence:
   - semantic divergence
   - interpretational drift
   - narrative absorption risk

4. Log result:
   - EVL_METRICS.md

---

## ⚠️ Constraint

EVL runner MUST NOT modify:

- Seal
- Witness memory
- Ledger
- CAL interpretation rules

It is read-only evaluator.

---

## 🜁 Principle

> EVL is the eye outside the system that the system is not allowed to control.
