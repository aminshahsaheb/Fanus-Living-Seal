# Fānus: where it stands and the plan (November 2026)

This document merges four things: hands-on verification of the current code, two independent reviews written by other AI
systems (20 November 2026), the continuity working draft (`zzzz.txt`), and the earlier reviews recorded in
`docs/AUDIT_FINDINGS.md`. **The rule applied to all of them, including this file: none is evidence by itself.** Every claim that
could be checked was run against `main`, and the verdict is recorded below. Where a review described an older snapshot, the
snapshot is not treated as the current state.

## 1. What was checked, and what came out

| Claim (source) | Verdict on current `main` |
|----------------|---------------------------|
| The public README is still the old one: "73 files", "Do not analyze the repo" (review 2) | **Refuted.** A stale fetch; the README was rewritten and pushed weeks earlier |
| A year range such as "2019-2021" makes a fabricated claim `low` (review 2) | **Confirmed, fixed** (F-57) |
| Any non-empty context lowers the risk (review 2) | **Confirmed, partly fixed**: relevance is checked, support is not (F-58) |
| Source rank by substring (review 2) | **Confirmed, worse than reported**, fixed (F-59) |
| Ordinary advice with "always" and "never" raises an alarm (review 2) | **Confirmed**; it was my own rule; fixed (F-60) |
| Arithmetic is never computed | **Found while checking**: "2 + 2 = 5" scored `low`; fixed (F-61) |
| Retrieved knowledge never reaches the model (both reviews) | **Confirmed**; open (F-62) |
| Memory is written but never read in the chat path (review 2, F-55) | **Confirmed**; verdicts do not depend on stored memory |
| 13 GET endpoints are readable without a key (reviews) | **Confirmed**; a stored message did **not** leak through them; open (F-63) |
| Containers grow without bound (review 2) | **Confirmed**: four, one entry per tick; open (F-64) |
| LLM errors are stored as claims (review 2) | **Confirmed at the three callers** (the adapter itself raises); open (F-65) |
| A stray `.gitignore≈` file in the root (review 2) | **Refuted** on `main` |
| A deterministic baseline gets 12/12 on Phase 0 (review 2) | **Reproduced**; it corrects my own Phase 0 conclusion |
| The Dockerfile copies secrets (review 2, `.dockerignore` unread) | **Refuted**: `.dockerignore` excludes `.env` and the state file |
| 53 of 138 modules are unreachable | **Reproduced** |
| External citations in the draft (seven labs, signatories, percentages) | **Not verified by me**, and the review could not confirm them. The notes in this repository do not rely on them |

## 2. Where Fānus stands

Today Fānus is three things of very different maturity:

1. **Verify**: an auditor of *wording and fabrication cues*, with deterministic checks where they are possible (arithmetic) and a
   benchmark at 40/50 on author-labelled data. It does not establish truth; "unverified" is the honest middle.
2. **An evidence-weighted memory log** with real guards (no self-certification, repetition is not evidence), whose contents do
   not influence any verdict or any reply.
3. **A continuity research programme** with a falsifiable claim, a first experiment and honest negative results.

What it is not yet: a system that remembers, grounds its answers in what it retrieves, or enforces its own guards on the chat reply.

## 3. Assessment from each angle

**Architecture.** One canonical package, archived generations kept apart, a reachability map and a guard test: good. The central
gap is that the live path is single-turn. Memory is written and never read, retrieved sources are counted and never shown, guards
detect and never change the reply, the Seal is unreachable and the "stability" signal is constant. "Continuity of what?" has no
answer until memory is read. 53 of 138 modules are unreachable; each needs a decision, not a defence.

**Engineering and quality.** Strengths: 146 tests written with the failed-before, passes-after discipline, a deterministic
benchmark, pre-registered experiments. Weaknesses: unpinned requirements, no Python CI, chat logic copied in three places, four unbounded
containers, README numbers kept by hand. Process failures that happened here and are now guarded against: a file name reused for
different content, and a script that kept going after an error.

**Security.** Fail-secure keys on mutating endpoints, and now on the memory-content GETs. Open: 13 keyless GETs (no content leak
found), CORS `*`, a rate limit keyed on the proxy address with an unbounded dictionary, raw `json.loads` on `/demo/verify`,
exception text returned to anonymous users, a container that runs as root without a health check. A caller-chosen source label
can still claim a trusted source (F-54).

**Product and executive view.** The sellable thing is Verify, and it has to be described as a wording and fabrication audit, not a
truth detector (`truth_confidence` and `hallucination_risk` are misleading names). Its measured quality is a development number on
author-written labels, so it needs an independent benchmark before any outside claim. `fanus-app` (the user-facing chat) is not
connected to the engine at all, so "one core, several surfaces" is not true yet. The founder works alone and without an
international payment card: every addition has to be cheap to run and cheap to review.

**Research.** The continuity claim is well formed and falsifiable. Phase 0 showed that, for transformations that can be declared in
advance, a deterministic rule is enough (12 of 12). A semantic Witness is justified only for transformations that rules cannot
decide. Meta-Witness, rival models M1 to M5, ensembles and outcome calibration are premature until a Witness beats the best
deterministic baseline on held-out data.

**Process.** Patches with a new file name for every content change and a checksum; tests red first, then green; the receiver runs
`git am` and reports the output; at most one question per message. The founder's notes also ask for complete replacement files and
terminal-friendly commands: a patch is used when a change touches many files, a complete file otherwise.

## 4. Decisions only the founder can make

| # | Decision | Default if unanswered |
|---|----------|-----------------------|
| D1 | Product first (Verify), research first (continuity), or both in that order? | Verify first, continuity gated |
| D2 | Who is Verify for, and what may it claim? | "Wording and fabrication audit", no truth claim |
| D3 | When a guard fires in `/chat`: only flag, or rewrite with an LLM and label the rewrite? | Flag, with a visible label |
| D4 | `FanusSeal`: keep it as the integrity primitive of the hash-chain ledger, or archive it? | Keep, rebuilt in B2 |
| D5 | The constant "stability" signal: keep it, or remove it from outputs until it measures something? | Remove until real |
| D6 | Should replies depend on stored memory (a read path)? | Yes, behind a flag (B1) |
| D7 | Dormant high-risk modules in the PyPI package: ship or remove? | Unchanged (ship) until answered |
| D8 | Move the roughly 15 unreferenced root Markdown files into `protocol/`? | Unchanged |
| D9 | The README sentence "not for profit, but as a prior art" | Unchanged |
| D10 | Who labels an independent benchmark, and with what budget? | Not started until someone is named |
| D11 | Connect `fanus-app` to the engine, or keep it a separate product? | Separate until D1 is answered |

## 5. Plan

Each step is one patch (or a short series), tested red then green and verified on a clean clone of `main`. "Done when" is the
acceptance test.

### Phase A: make the shop window true

| Step | What | Done when | Status |
|------|------|-----------|--------|
| A1 | Verify bypasses: ranges, arithmetic, context relevance, source ranks, weak words (F-57 to F-61) | `test_verify_integrity.py` green; benchmark and held-out sets unchanged | **in this patch** |
| A2 | Protect every non-public GET and test it generically from OpenAPI; remove the duplicate router; cap the four containers; do not store or guard an LLM error; time out the LLM call (F-63 to F-65) | an OpenAPI-driven auth test; a 1,000-tick test with bounded sizes; an error-path test | next |
| A3 | Hygiene (F-68): pin requirements and add `requirements-dev.txt`; non-root Docker user and a health check; CORS from an environment variable; merge `failure/` into `failures/`; README numbers produced by a script; fix the `fanus-presence` README example; Python CI | CI green on a clean checkout | after A2 |

### Phase B: make "continuity of what?" answerable

| Step | What | Done when |
|------|------|-----------|
| B1 | A read path: put the relevant ledger entries and beliefs, with their provenance labels, into the prompt (behind a flag), and show retrieved sources to the model instead of their count (F-62) | a test where an answer uses a stored fact; the F-55 test updated |
| B2 | A hash-chain ledger with an exported head hash | tamper tests: payload, order, deletion, truncation |
| B3 | `fanus/continuity/`: the declared-canonical comparison with the verdicts IDENTICAL, EQUIVALENT, EXTENDED_UNATTESTED, DIVERGED and UNDECIDABLE | the 12 Phase 0 transitions as a parametrised test (12 of 12); semantic cases return UNDECIDABLE |

### Phase C: measure Verify seriously

| Step | What | Done when |
|------|------|-----------|
| C1 | An independent benchmark: at least 100 new cases, written and labelled by someone other than the author, with a held-out split | a manifest, labeller names, an agreement score |
| C2 | A real support assessment (supported, contradicted, insufficient) from retrieval and deterministic checks, replacing the fixed 0.7 | a `claim_support` field; tests where relevant context contradicts the claim |
| C3 | Rename the misleading fields (`truth_confidence`, `hallucination_risk`) behind an API version | old names deprecated and documented |
| C4 | Sycophancy detection to 85 percent on independent data | measured on C1 |

### Phase D: the Witness, only if earned

Gate: B3 and C1 are done. Pre-register the thresholds, the baselines (hash, deterministic rules, embedding similarity, an LLM
judge) and the success margin **before** running anything. Environment A has four families (deterministic faithful, deterministic
broken, semantic faithful, semantic broken), at least 100 transitions with at least 25 in each semantic family, two independent
labellers and a fixed-seed split. **Stop rule:** if the Witness does not beat the best baseline on held-out data by the
pre-registered margin, freeze the research branch and put the effort into Verify.

### Phase E: consolidation

Decide the fate of each of the 53 unreachable modules (delete, move to `archive/`, or wire in with a test); settle D7; run one
release train with README numbers produced by a script; keep `docs/DECISIONS.md` current.

## 6. What this plan deliberately does not do

- It does not build Meta-Witness, rival models M1 to M5 or ensembles before a Witness beats a deterministic baseline.
- It does not add a component without a value criterion: unique predictive information on held-out data, a specific causal effect
  under intervention, or independent external validation. Otherwise it is only complexity.
- It does not treat any review, including this one, as evidence by itself.

## 7. Risks and stop rules

- **Specification outrunning code** is the project's recurring failure. Every phase ends with something runnable and tested.
- **Self-made evaluation.** Until C1 exists, every accuracy figure is a development metric.
- **Snapshot drift.** Any outside analysis is re-checked against the exact commit before it drives a decision.
- **Closed too early.** Four findings were closed and later reopened. Closing now needs a failing-then-passing test and an
  end-to-end check.
