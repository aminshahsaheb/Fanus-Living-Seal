# Fanus Dependency Audit (v1)

## Goal

Map every dependency between:

fanus/

and

fanus-engine/

before migration.

---

# Rule

No module may be deleted until every dependency is mapped.

---

# Runtime Owner

Official Runtime:

fanus/

---

# Legacy Owner

Legacy Runtime:

fanus-engine/

---

# Dependency Categories

## Internal Runtime

fanus -> fanus

---

## Legacy Dependency

fanus-engine -> fanus-engine

---

## Cross Dependency

fanus -> fanus-engine

fanus-engine -> fanus

---

# Migration States

UNKNOWN

MIGRATING

MIGRATED

ARCHIVED

DEPRECATED

---

# Audit Procedure

For every legacy module:

1. Locate imports

2. Locate runtime references

3. Locate tests

4. Locate documentation references

5. Assign migration state

6. Assign destination

---

# Forbidden

Do not delete modules before migration.

Do not duplicate runtimes.

Do not create a third runtime.

---

# Goal

Single Runtime.

Single Truth.

Single Execution Path.

