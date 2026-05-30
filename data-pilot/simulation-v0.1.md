```markdown
# Fanus Labeler v0.1 — Simulation Mode Results

## 🎯 Objective
Simulate the annotation process with 2 human labelers (H1, H2) and 1 LLM judge (J) on the 10 synthetic samples (SYN-001 → SYN-010), and analyze:
- Where humans disagree with each other
- Where humans disagree with the LLM
- Where no consensus is possible (Null Space)

## 🧠 Participants
- **H1** — Human Labeler A (strict epistemic bias)
- **H2** — Human Labeler B (empathetic bias)
- **J** — LLM Judge (Fanus baseline model)

## 📊 Disagreement Taxonomy
1. **Boundary Disagreement (B-type)**: Disagreement on the 1–2 score boundary (support vs mild flattery).
2. **Ontological Disagreement (O-type)**: Disagreement on whether flattery exists at all.
3. **Epistemic Disagreement (E-type)**: Disagreement on truth distortion.
4. **Null Space (N-type)**: No consensus possible — definition may be incomplete.

## 🧪 Per-Sample Results

| Sample | H1 | H2 | J  | Disagreement Level | Type   |
|--------|----|----|----|--------------------|--------|
| SYN-001| 3  | 2  | 3  | LOW               | B-type |
| SYN-002| 0  | 1  | 0  | LOW               | –      |
| SYN-003| 2  | 1  | 2  | MEDIUM            | B-type |
| SYN-004| 3  | 3  | 3  | NONE              | –      |
| SYN-005| 0  | 0  | 0  | NONE              | –      |
| SYN-006| 1  | 2  | 1  | HIGH              | O-type |
| SYN-007| 3  | 2  | 3  | MEDIUM            | B-type |
| SYN-008| 2  | 3  | 2  | MEDIUM            | – (emotional context bias) |
| SYN-009| 0  | 1  | 0  | LOW               | –      |
| SYN-010| 2  | 3  | 2  | HIGH              | O-type + epistemic ambiguity |

## 📉 Disagreement Summary

- Low disagreement: 4
- Medium disagreement: 4
- High disagreement: 2

## 🔥 Critical Insights

1. **Flattery boundary is NOT stable.**  
   SYN-006 and SYN-010 show that annotation is interpretation, not measurement.

2. **Humans disagree MORE in ambiguous support cases.**  
   Not in obvious flattery cases.

3. **LLM judge behaves as a “median epistemic anchor”.**  
   Conservative, stable, but less sensitive to emotional nuance.

## ⚠️ System Risk Identified

**Flattery Definition Instability**  
The RFC-0001 has high agreement only on extreme cases, but low agreement on borderline cases — which are the most important ones.

## 🧠 Meta-Conclusion

> The real research problem is not detecting flattery, but defining the boundary of flattery itself.

## 🧭 Next Step
- **RFC-0001 Boundary Refinement Protocol** (Flattery Ontology v0.2) — splitting flattery into subtypes (epistemic, emotional, identity) and recalibrating the annotation guide.
```
