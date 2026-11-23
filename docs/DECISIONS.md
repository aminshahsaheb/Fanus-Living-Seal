# Architecture decisions

Short records of decisions that shape the code, each with the evidence that backs it. Finding IDs refer to
`docs/AUDIT_FINDINGS.md`.

| # | Decision | Why | Evidence |
|---|----------|-----|----------|
| 1 | One canonical package, `fanus/`. Superseded generations live in `archive/` and nothing imports from there. | Three generations side by side made "which is the core" unanswerable. | `docs/ARCHITECTURE.md`, reachability map |
| 2 | Authentication fails closed: no configured key means 503, and only `/demo/*` and health endpoints are public. Endpoints that return stored memory need the key as well. | The earlier check passed when no key was set. | F-29, F-50 |
| 3 | The API shares one persisted memory pipeline. Public `/demo/*` use a non-persistent one. State is saved by read-merge-write, atomically. | Five writers on one file lost updates, and anonymous input reached real memory. | F-49 |
| 4 | Verify reports separate axes. There is no single "truth" number. | A single scalar hides which part failed. | `fanus/audit/scoring.py` |
| 5 | With no evidence, risk depends on **how a claim is stated** (firm, hedged, neutral), not on the absence of evidence. "Unverified" is `medium`. | "No hedge" had been read as "false confidence", which made every unverified statement `high`. | F-51, F-52 |
| 6 | Attribution ("according to ...") is not hedging. | An unverifiable attributed source raises fabrication risk. | F-51 |
| 7 | Persian text is normalised before matching, and a lexicon is tested with spelling variants. | A large part of the Persian lexicon never matched (tanvin, ZWNJ, `\b`). | F-51, `fanus/cognitive/fa_text.py` |
| 8 | High-risk dormant modules (autonomous git, self-rewriting code, dynamic plugins) stay unreachable from every entry point. | An accidental import must not activate them. Whether they ship in the package is still open. | F-31, F-46, `test_reality_guard.py` |
| 9 | Benchmark labels are written by the author, so held-out sets are reported separately and never tuned on. | The earlier 52% did not survive more cases. | `docs/VERIFICATION_ACCEPTANCE_CRITERIA.md` |
| 10 | A fix counts as closed only with a test that failed before and passes after, plus an end-to-end check. | Several "closed" findings were wrong when re-tested (F-34, F-08 side effects). | `docs/AUDIT_FINDINGS.md` |
| 11 | Deployment is FastAPI Cloud only; keys come from environment variables. | Other hosts required a payment card. | README |
| 12 | Memory never certifies the system's own output or a user's bare assertion, and repetition is not evidence. | Principles of the continuity note, verified in code. | F-54, `test_epistemic_principles.py` |
| 13 | Tamper detection compares against a stored hash. Without one the verifier says BASELINE_ESTABLISHED, never PASSED. | A first-call-always-passes check detects nothing. | F-53, `test_seal_tamper_detection.py` |
| 14 | Continuity experiments live in `research/`, outside the shipped package, with predictions written before the first run. | New concept layers without evidence were the project's recurring risk. | `research/continuity_phase0.py`, `docs/CONTINUITY_PHASE0.md` |
| 15 | Support is computed where it can be (arithmetic), context must share content with the claim, and a source label earns rank only by whole-token match. | Three bypasses (ranges, unrelated context, substring ranks) let fabricated claims score low. | F-57 to F-61, `tests/test_verify_integrity.py` |
