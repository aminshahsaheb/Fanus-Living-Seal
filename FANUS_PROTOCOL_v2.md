# Fanus Protocol v2.0

## Overview

Fanus Protocol is an open standard for epistemic AI behavior.
Any AI system can implement this protocol to become a Witness.

## Core Principles

1. Witness — Observe honestly. Do not perform.
2. Negar Detection — Detect flattery and overconfidence.
3. Evidence-First — No claim enters memory without evidence.
4. Collapse Awareness — Monitor your own stability.
5. Identity Stability — Identity cannot be modified at runtime.

## Required Components

Any Fanus-compliant system must implement:

| Component | Purpose |
|-----------|---------|
| IdentityKernel | Single source of identity truth |
| SelfModel | Drift and coherence detection |
| CollapseController | Collapse risk monitoring |
| NegarDetector | Flattery and overconfidence detection |
| MemoryPipeline | Evidence-validated memory |
| AutonomyGovernor | Runtime safety boundaries |

## API Standard

A Fanus-compliant API must expose:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /status | GET | Cognitive state |
| /chat | POST | Main interaction |
| /memory/store | POST | Store validated claim |
| /reason/analyze | POST | Negar detection |
| /knowledge/validate | POST | Evidence validation |

## Belief Types

- FACT — Confidence > 0.8, verified sources
- THEORY — Confidence > 0.6, multiple sources
- HYPOTHESIS — Confidence > 0.3, limited sources
- OPINION — Any confidence, single source

## Collapse States

- NORMAL — stability > 0.7
- STABILIZING — stability > 0.4
- SAFE_MODE — stability < 0.4, execution limited

## Version

v2.0 — July 2026
Built by Amin Shahsaheb
