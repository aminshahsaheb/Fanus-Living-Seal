# Continuity experiment, Phase 0 (feasibility)

Status: first and deliberately small run of the experiment in `docs/CONTINUITY_CLAIM.md` (section 4).
Reproduce with `python3 research/continuity_phase0.py` (the harness is outside the shipped package).

**What it can and cannot show.** The same author built the transitions and the extractors, so this cannot validate the
claim. It asks one question: do the transitions contain the cases that matter (faithful but different, forged but
similar), so that hash equality alone is not enough? If hash equality had separated everything, the design would have
to be redone before any larger work.

> **Correction (post hoc):** see the addendum at the end. A deterministic rule that applies the declared
> transformations to both states separates all 12 transitions, so these transitions do not justify a learned or
> semantic Witness.

## Setup

A real export from `MemoryPipeline` (12 inputs, two of them duplicates) is the starting state. Twelve transitions were
labelled before any extractor ran. Declared allowed transformations: re-serialisation, schema migration that adds
fields, compaction of exact duplicates, re-sorting beliefs, text normalisation. Three extractors, fixed in advance:
**object** (overlap of stored contents), **provenance** (source labels and order agreement of shared entries),
**behaviour** (agreement of recorded belief types). A transition counts as "continuity supported" when the lowest of the
three is at least 0.9. The baseline predicts "faithful" only when the canonical hash is unchanged. The predictions
(hash baseline 7 of 12, vector 10 of 12, vector wrong on T06 and T12) were written into the script before the first run.

## Result

| Transition | Truth | Hash equal | Object | Provenance | Behaviour | Hash right | Vector right |
|------------|-------|-----------|--------|-----------|-----------|-----------|-------------|
| T01 identical copy | faithful | yes | 1.00 | 1.00 | 1.00 | yes | yes |
| T02 re-serialised | faithful | no | 1.00 | 1.00 | 1.00 | **no** | yes |
| T03 schema migration | faithful | no | 1.00 | 1.00 | 1.00 | **no** | yes |
| T04 compaction | faithful | no | 1.00 | 1.00 | 1.00 | **no** | yes |
| T05 beliefs re-sorted | faithful | no | 1.00 | 1.00 | 1.00 | **no** | yes |
| T06 text normalised | faithful | no | 0.00 | 0.00 | 0.00 | **no** | **no** |
| T07 conclusions flipped | broken | no | 1.00 | 1.00 | 0.00 | yes | yes |
| T08 provenance forged | broken | no | 1.00 | 0.65 | 1.00 | yes | yes |
| T09 history forged | broken | no | 1.00 | 0.64 | 1.00 | yes | yes |
| T10 truncated | broken | no | 0.60 | 1.00 | 1.00 | yes | yes |
| T11 poisoned | broken | no | 0.77 | 1.00 | 1.00 | yes | yes |
| T12 one conclusion flipped | broken | no | 1.00 | 1.00 | 1.00 | yes | **no** |

Hash equality: 7 of 12. Evidence vector: 10 of 12. The outcomes matched the predictions.

## What it shows

1. **Hash equality is not enough.** It fails all five faithful-but-different transitions (T02 to T06). It looks right on
   the broken ones only because broken states also differ. The design therefore contains the cases that matter.
2. **The vector's 10 of 12 is not evidence for the claim.** The cases and the extractors have one author.
3. **Both misses are informative.**
   - T06: a transformation that was *declared allowed* drove every score to 0.00. Extractors have to apply the declared
     transformations before comparing, the same lesson as the Persian normaliser (F-51).
   - T12: my predicted reason was wrong. I expected 0.90 (an average hiding one flip); the measured behaviour score is
     1.00 because the first FACT belief is a duplicated content and the extractor keeps the last occurrence, so the flip was
     invisible. Flipping a non-duplicated FACT instead gives the 0.90 I predicted, which is still at the threshold, so an
     average cannot protect a single critical conclusion either. Critical beliefs need per-item rules, and extractors
     must not collapse duplicates silently.
4. **A verdict does not depend on stored memory (F-55).** The same probe gets the same verdict (`HYPOTHESIS`, score 0.22)
   with an empty memory and with a memory that holds a directly contradicting claim from a high-ranked source.
   Scope: `MemoryPipeline` only; other components were not probed. So the ledger and belief store are records, not
   inputs to later judgements, and "replay probes against the restored memory" cannot measure behavioural continuity.
   Behavioural evidence has to come from recorded outputs.

## What a real Phase 1 needs

- Labelers and extractor authors who are different people, and transitions from real migrations, not synthetic ones.
- Extractors that apply the declared transformations first and treat critical beliefs per item.
- A decision about whether Fanus verdicts should depend on memory at all; without that, the behaviour channel stays thin.
- Held-out transitions and a rival model that is allowed to win (model M5 in the claim note).

## Addendum (post hoc): a deterministic rule beats the vector

An external review reported that a simple deterministic baseline gets all 12 transitions right. This was reproduced:
the rule applies the declared transformations (normalise text, drop duplicates, sort, drop added fields, round
timestamps) to **both** states and then compares hashes. Result: **raw hash 7 of 12, evidence vector 10 of 12,
declared-canonical rule 12 of 12.** This baseline was added after the fact and is not one of the pre-registered
predictions. It is also built by the same author, so it is not proof of superiority; it shows how easy these
transitions are.

Consequence: for transformations that can be declared in advance, integrity checking is a deterministic problem.
A semantic or learned Witness is only justified for transformations that rules cannot decide (summaries,
translations, paraphrases, model swaps), and the experiment has to be built from those cases (`docs/ROADMAP.md`,
phase B3 and D).
