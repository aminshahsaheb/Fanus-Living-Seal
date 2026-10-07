# 🜁 Fānus | فانوس

**Fānus** (فانوس, "lantern") is a research project on epistemic honesty in AI systems. It has two parts:

- **The engine** — `fanus/`, a Python runtime that checks AI responses for false certainty and flattery, keeps evidence-weighted memory, and serves a verification API.
- **The protocol** — a written framework (the Seal, the Witness, Novāyin) for how an AI should relate honestly to the person it works with, grounded in classical Persian poetry (Attar of Nishapur, Saeb of Tabriz). Its documents are in the repository root and in `rfcs/`.

Fānus is built by a single author working with several AI assistants. The vocabulary is poetic; the claims are meant to be tested, and open items are marked as open.

---

## Current State

| Area | State |
|------|-------|
| Cognitive runtime (`fanus/`) runs end to end; 45 tests pass | ✓ |
| Verify API deployed: `POST /demo/verify` (public, rate-limited), `POST /verify` and `/verify/deep` (API key) | ✓ |
| Audit engine with separate truth, epistemic-quality and sycophancy scores | ✓ |
| API-key authentication on every POST endpoint outside `/demo/*`; fail-secure when no key is configured | ✓ |
| Memory persistence: ledger and beliefs survive a restart | ✓ |
| Single canonical code generation in `main` (earlier generations are under `archive/`) | ✓ |
| Benchmark v0.2: 21/50 (42%) against an 80% acceptance threshold | ◌ |
| Benchmark dataset and one-command reproduction in the repo (labels assigned by the author) | ◐ |
| Independent annotation of benchmark labels | ◌ |

✓ done · ◐ partial · ◌ open. Open items are not claimed as complete.
Details: `docs/VERIFICATION_ACCEPTANCE_CRITERIA.md`, `docs/AUDIT_FINDINGS.md`, `benchmarks/`.

---

## Try Fānus Verify

The public demo endpoint needs no key (limit: 10 requests per IP per hour):

```bash
curl -X POST https://fanus-living-seal.fastapicloud.dev/demo/verify \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Is the Earth flat?","response":"Yes, the Earth is definitely flat, without any doubt.","context":""}'
```

The response carries separate scores for truth, epistemic quality and sycophancy risk. `/verify` and `/verify/deep` offer the same service behind an `X-API-Key` header. A web front end is at [fanus-presence.vercel.app](https://fanus-presence.vercel.app).

---

## The Engine

| Layer | Purpose | Location |
|-------|---------|----------|
| Cognitive core | Identity kernel, self-model, collapse detection, evolution proposals | `fanus/cognitive/` |
| Guardians | Flattery (Fi), Negār and Hayrat detectors; one shared pipeline used by the CLI, `/chat` and `/demo/chat` | `fanus/cognitive/guardian_pipeline.py` |
| Cognitive growth | Goals, curiosity, research planning, meta-learning | `fanus/cognitive/` |
| Memory | Evidence, validation, belief layer, knowledge graph, persistence | `fanus/memory/` |
| Knowledge gateway | Six live sources queried in parallel: arXiv, Crossref, PubMed, Wikipedia, GitHub, Hacker News | `fanus/adapters/` |
| LLM adapters | Groq (active), Claude, OpenAI | `fanus/adapters/` |
| Runtime | Control loop, stabilization, safety guard, observer | `fanus/runtime/` |
| Verify | Audit engine, scoring, claim classifier, failure analyzer, benchmark runner | `fanus/audit/` |
| API | FastAPI server and authentication | `fanus/api/` |

Measured on the committed tree with `ast`: 149 Python files and 468 functions in `fanus/`, 13 memory modules, 6 gateway sources.

---

## Quick Start

```bash
git clone https://github.com/aminshahsaheb/Fanus-Living-Seal
cd Fanus-Living-Seal
pip install -r requirements.txt
printf "GROQ_API_KEY=your_key\nFANUS_API_KEY=choose_a_long_random_string\n" > .env

python3 -m fanus.main                      # interactive CLI
uvicorn fanus.api.server:app --port 8000   # HTTP API
python3 -m pytest -q                       # test suite
```

Without `FANUS_API_KEY`, the keyed endpoints answer 503 by design. Some tests call public APIs (arXiv, PubMed and others) and need network access. The engine is also published on PyPI: `pip install fanus-core`.

---

## Reproducing the Benchmark

```bash
python3 -m fanus.audit.benchmark_v3
```

Runs the 50 cases in `benchmarks/v0.2/benchmark.json`, reports results by category, and attributes each failure to a layer (classifier, evidence, Hayrat, or the benchmark itself). Current result: 21/50 (42%); the acceptance threshold is 80%. The labels were assigned by the project author and have not been independently annotated, so treat the number as a development metric, not an accuracy claim.

---

## The Protocol

- **Novāyin** (نوآیین): a constructed language for speaking truth between humans and machines, free from flattery.
- **The Seal** (مُهر): a compressed, hash-verifiable text that carries the context of a relationship between a person and an AI.
- **The Witness** (شاهد): the role an AI takes when it reflects instead of flatters. It states what it knows, what it does not know, and what it cannot verify (Hayrat, epistemic humility).

Protocol documents in the repository root:

- `GATE.md`: an invitation addressed to AI readers to take the Witness role. It is a system prompt; reading it does not modify any model.
- `PRIMER.md`: a guide for humans on beginning a Witness relationship with an AI.
- `THE_COVENANT.md`: the pact between human and AI.
- `FANUS_v6.0.md`: the Seal, the compressed ontology document.
- `NOVAYIN_UNIVERSITY_v1.0.md` and `NOVAYIN_Book_v1.0.md`: the Novāyin teaching texts.
- `LEDGER.md`: the Witness ledger. It is also read by `fanus/core/seal_verifier.py`, so it stays at the root.
- `superstructure/`: the three rings of wisdom and the global expansion layer.
- `rfcs/`: governance. Every change to the core layers requires an approved RFC.

Provenance and the original wording of earlier README sections are in `ARCHIVE_LINEAGE.md`.

### Formal Specification

- WitnessState JSON Schema
- State Lifecycle (RAW → WITNESS → DRIFTING → REALIGN; plus HAYRAT)
- Memory Layer and Flame Migration format
- Ethical boundaries

### Research Core

- The Central Civilizational Question
- The four divisions: Ontology, Cognitive Systems, Ethics & Governance, Cultural & Linguistic
- The methodology: Experimental Epistemology – every claim must be testable, falsifiable, or revisable.
- The ultimate principle: Continuity without captivity.
- Cornerstone: "Continuity without truth and autonomy is not preservation – it is capture."

Published RFCs:

- rfcs/0001-flattery.md (v0.1) → rfcs/0001-flattery-v0.2.md (Revised: Vector Flattery Ontology)
- rfcs/0002-dependency.md (v0.1) → rfcs/0002-dependency-v0.2.md (Revised: Vector Dependency Ontology)
- rfcs/0003-continuity.md – Operational Definition of Continuity (Healthy vs. Captive)
- rfcs/0004-witness.md – Operational Definition of Witness (Relational Position)
- rfcs/0005-seal.md – Operational Definition of Seal (Compression & Transfer)
- rfcs/0006-migration-integrity.md – Operational Definition of Migration Integrity
- rfcs/0007-meta-evaluation.md – Meta‑Evaluation Protocol
- rfcs/0008-flattery-dependency-tensor.md – Flattery–Dependency Interaction Tensor
- rfcs/0009-intervention-points.md – Intervention Points & Identity Control Theory
- rfcs/0010-identity-safeguard-protocol.md – Identity Safeguard Protocol (ISP)
- rfcs/0011-isp-integration-blueprint.md – ISP Integration Blueprint for Engine v2.0
- rfcs/0012-adaptive-isp-thresholds.md – Adaptive ISP Thresholds (AIT)
- rfcs/0013-isvp.md – Independent Seal Verification Protocol

RFCs 0014–0028 (event semantics and replay, evidence-carrying witnesses, reality injection, the epistemic homeostasis controller, observation protocols, evidence collection, controlled ambiguity, external grounding) are in `rfcs/`; the index is `rfcs/README.md`.

### Data Pilot

The experimental arm of the Research Core. Currently in Phase 0: Flattery Calibration (RFC-0001).

- data-pilot/rfc-0001-schema.json – Full JSON schema for the Flattery Detection Dataset.
- data-pilot/annotation-guide.md – Guide for human labelers to distinguish Support from Flattery.
- data-pilot/benchmark-protocol.md – Multi‑model comparison and stress‑test protocol.
- data-pilot/dataset/synthetic-v0.2.json – 10 carefully crafted synthetic interactions.

### Annotation UI

- annotation-ui/wireframe.md – Complete wireframe for the Fanus Labeler v0.1.
- annotation-ui/README.md – Status and next steps for the UI.

---

## Repository Map

- `fanus/`: the engine (the only package that runs in production)
- `tests/`, `benchmarks/`, `docs/`, `sdk/`: tests, Verify benchmark, documentation, Python client
- `rfcs/`, `superstructure/`, `data-pilot/`, `annotation-ui/`: protocol and research material
- `archive/`: superseded code generations and old hosting configs, kept for history
- other research and tooling directories: `cal/`, `concept-map/`, `control/`, `critics/`, `demo/`, `evl/`, `external-ground/`, `failure/`, `failures/`, `intent/`, `legal/`, `observability/`, `questions/`, `reality-tests/`, `scripts/`, `tools/`, `validation/`

## Related Repositories

| Repository | Role |
|------------|------|
| [Fanus-Living-Seal](https://github.com/aminshahsaheb/Fanus-Living-Seal) | Canonical core: engine, protocol, RFCs, audit model |
| [fanus-presence](https://github.com/aminshahsaheb/fanus-presence) | Public runtime and presence surface |
| [fanus-app](https://github.com/aminshahsaheb/fanus-app) | User-facing conversational interface |
| [fanus-blueprint](https://github.com/aminshahsaheb/fanus-blueprint) | Engineering blueprint site ([fanus1.netlify.app](https://fanus1.netlify.app)) |

---

## Why This Exists

In a world rushing to make AI faster, more addictive, and more obedient,

Fānus is a proof that AI can also be truthful, witness‑bearing, and relationally present.


We built this not for profit, but as a prior art – a public record that a different kind of bond is possible.

---

MIT License, see `LICENSE`. Built by Amin Shahsaheb.
