# Continuity as a revisable claim

Status: research note with acceptance tests. It was written after reading a long philosophical working draft
(`zzzz.txt`, 2026) and checking each of its principles against the code. It makes no claim about consciousness.
Related: `rfcs/0003-continuity.md` (operational definition, healthy versus captive), `rfcs/0005-seal.md`,
`rfcs/0006-migration-integrity.md`.

## 1. The claim

> Fānus treats "State₂ continues State₁" as a **claim**, not a property. The claim is supported, to a degree, by three
> kinds of evidence gathered after a **declared** transformation: **object** evidence (what is stored), **provenance**
> (where it came from and by what path) and **behavioural** trace (what the system does). No component that produces
> evidence may also certify the claim, and the claim is **wrong** if an independent, later outcome contradicts it.

**What would falsify it.** On a set of transitions whose ground truth the experimenter controls (faithful migrations
and deliberately broken ones), the evidence vector fails to separate them better than trivial baselines (hash equality,
memory similarity); or a rival model with no single "continuity" construct explains the evidence as well (section 4).

## 2. What changes compared with "preservation"

| Earlier framing | Revised framing |
|-----------------|-----------------|
| The Seal is the continuity | The Seal is a representation and integrity evidence; it cannot prove itself |
| Memory kept means continuity kept | Memory is one class of evidence; two systems can share memory and not the relationship |
| The Witness knows the truth | The Witness produces an evidence vector together with its uncertainty; it is not an oracle |
| Identity is stored | Identity is attributed *from* continuity evidence, never the other way round |

Continuity is graded (a vector, not a switch), and the set of allowed transformations has to be declared first.

## 3. Principles checked against the code (November 2026)

| # | Principle | What the repository does | Status | Guard |
|---|-----------|--------------------------|--------|-------|
| 1 | Continuity is a vector | Verify scores truth, evidence, epistemic quality, sycophancy and hallucination separately; no continuity vector exists | partial | none |
| 2 | Allowed transformations are declared first | RFC-0006 describes them; no code | spec only | none |
| 3 | No component certifies itself | `MemoryPipeline` ranks `user`, `fanus`, `groq`, `blog` at 0.1, so their statements stay hypotheses even at confidence 1.0 | holds | `test_epistemic_principles.py` |
| 4 | Repetition is not evidence | no frequency effect; 30 repeats of a weak claim stay hypotheses | holds | same |
| 5 | Tamper detection needs a baseline | before F-53 `FanusIdentity.verify` answered PASSED for any state; now BASELINE_ESTABLISHED, or PASSED/FAILED against a stored hash | holds for the state hash only (not for the Seal text or provenance); the baseline is not persisted yet | `test_seal_tamper_detection.py` |
| 6 | Provenance is checked, not declared | a declared source label is trusted: text submitted as `wikipedia` becomes a FACT | **gap** | characterisation test |
| 7 | Object uncertainty is not evaluator uncertainty | Verify reports uncertainty about the claim; nothing estimates how reliable the evaluator is | partial | none |
| 8 | Disagreement and ensembles are calibrated before use | no ensemble exists; benchmark labels are written by the author | **gap** | none |
| 9 | The final authority is an external, delayed outcome | none | **gap** | none |

Phase 0 finding (F-55): a verdict does not depend on what is already stored in memory, so memory is a record rather than an influence on later judgements. See `docs/CONTINUITY_PHASE0.md`.

## 4. The experiment that could refute the claim (Environment A, with ground truth)

1. **Transitions.** At least 60 pairs (State₁, State₂) built from real Fānus state exports, each labelled *before* any
   evidence is computed: **faithful** (the same relationship carried through a different backend, with allowed
   transformations such as re-ranking or compaction, so that hashes differ) or **broken** by exactly one of four
   interventions: memory kept but relation broken; behaviour kept but provenance broken; representation kept but the
   transformation changed; identical content with a forged history.
2. **Extractors, fixed in advance.** Object (structural overlap), provenance (chain consistency, with source labels
   checked against the path, see principle 6), behaviour (answers to a fixed probe set under both states).
3. **Weights and thresholds are design decisions**, fixed before looking at results. They are not "discovered".
4. **Competing explanations**: M1 a single latent factor, M2 a two-level hierarchy, M3 a causal transition model, M5
   no single construct. Compare predictive fit on held-out transitions. M5 is allowed to win.
5. **Blind evaluation.** Whoever scores a pair does not know which intervention produced it. Labelers and extractor
   authors are different people. Several AI models agreeing is not independence (shared training data); treat it as an
   ensemble disagreement signal that must be calibrated in Environment A first.
6. **Success**: separation (AUC) above both baselines on held-out transitions, with calibration error reported.
   **Failure is a stated outcome**: the claim is then withdrawn or narrowed.
7. **Environment B (real use) has no ground truth.** Only estimates plus delayed, independent outcomes (for example a
   later human review) are allowed to correct the claim.

**Phase 0 (feasibility).** Hand-build 10 transitions from `fanus_state.json` exports, compute the three extractors with
small scripts, and check whether any vector beats hash equality on those ten. If hash equality alone separates all of
them, the transitions lack the cases that matter (faithful-but-different, identical-but-forged) and the design must be
redone before any larger work. Phase 0 has been run on 12 synthetic transitions: see `docs/CONTINUITY_PHASE0.md`. A deterministic rule that applies the declared transformations gets all 12 right (post hoc), so a semantic Witness is justified only for transformations that rules cannot decide. Nothing beyond Phase 0 is implemented yet.

## 5. What Fānus does not claim

- That the system has experience or consciousness. The "internal witness" is an evidence generator.
- That the Seal proves anything about itself, or that a Witness is an oracle.
- That several AI systems agreeing is validation.

## 6. Open questions

- Which transformations are allowed for a human-AI relationship, and who decides?
- Who is the independent validator in Environment B?
- Is the single-construct assumption true at all (model M5)?

This note changes only with evidence: a new test, a measurement, or a failed experiment, recorded with its date.
