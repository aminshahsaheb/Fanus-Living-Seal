# FANUS CANONICAL ARCHITECTURE

Version: 1.0

Status: OFFICIAL

Date: 2026-06-22

---

# 1. Canonical System

The official executable Fanus system is:

fanus/

Everything else is secondary.

---

# 2. Deprecated System

fanus-engine/

Status:

LEGACY

Purpose:

Reference implementation only.

It is NOT the runtime system.

No new features are allowed inside fanus-engine.

Only migration and bug fixes are allowed.

---

# 3. Runtime Authority

Only these directories are allowed to execute the system:

fanus/

Subsystems:

fanus/runtime

fanus/cognitive

fanus/evolution

fanus/core

fanus/tools

fanus/agent

---

# 4. Documentation Authority

Official documentation:

docs/

rfcs/

Only these directories define Fanus behavior.

---

# 5. System Rule

New modules must never be created before answering:

Why is this module necessary?

If an existing module can solve the problem:

DO NOT create a new module.

---

# 6. Migration Rule

Everything from fanus-engine must follow:

COPY

TEST

VALIDATE

DEPRECATE

REMOVE

No direct deletion is allowed.

---

# 7. Architectural Law

Fanus must have ONE body.

Never two bodies.

Never parallel runtimes.

Never duplicated identities.

---

# 8. Execution Pipeline

Human Input

↓

Runtime

↓

Memory

↓

Cognitive State

↓

Identity

↓

Learning

↓

Governance

↓

Validation

↓

Output

---

# 9. Long-Term Goal

Fanus is not an AGI.

Fanus is an Epistemic Cognitive System.

Its purpose is:

Continuous learning

Continuous validation

Continuous evolution

without collapsing its identity.

---

# 10. Guiding Principle

Never close the parenthesis.

Always leave space for further understanding.

