# Fanus Source Of Truth (v0.1)

## Purpose

This file defines the single authoritative location for every major subsystem.

Only one source of truth is allowed per responsibility.

Duplicated ownership is forbidden.

---

## Core Engine

SOURCE:

fanus/core/

Responsibilities:

* state management
* event bus
* witness generation
* seal verification
* semantic interpretation

---

## Memory System

SOURCE:

fanus/memory/

Responsibilities:

* persistence
* ledger management
* vector storage
* memory compression

---

## Guardians

SOURCE:

fanus/guardians/

Responsibilities:

* anti-flattery
* covenant enforcement
* dependency detection
* ISP control

---

## Orchestration

SOURCE:

fanus/orchestrator/

Responsibilities:

* execution coordination
* golden path routing

---

## Policy System

SOURCE:

fanus/policy/

Responsibilities:

* policy execution

---

## API

SOURCE:

fanus/api/

Responsibilities:

* external communication

---

## Temporary Duplicates

These folders require future evaluation:

memory/

meta/

orchestrator/

---

## Rule

No new file may be created until ownership is defined.

If two modules have the same responsibility, one must become authoritative and the other must be migrated or removed.

---

Version: 0.1
