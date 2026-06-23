# FANUS MODULE MIGRATION MAP

## SOURCE OF TRUTH

Canonical Runtime:

fanus/

Legacy Runtime:

fanus-engine/

------------------------------------------------

STATUS LEGEND

KEEP

MIGRATE

REPAIR

ARCHIVE

DELETE

REVIEW

------------------------------------------------

## fanus-engine/fanus/core

witness_agent.py      -> MIGRATE
state_machine.py      -> MIGRATE
event_bus.py          -> MIGRATE
hayrat_judge.py       -> MIGRATE
semantic_layer.py     -> REVIEW
seal.py               -> REPAIR
seal_verifier.py      -> MIGRATE
presence_state.py     -> REVIEW
judgment_layer.py     -> REVIEW
meta_auditor.py       -> REVIEW
witness_auditor.py    -> REVIEW

------------------------------------------------

## fanus-engine/fanus/memory

vector_store.py           -> REVIEW
ledger.py                 -> REPAIR
persistence_manager.py    -> REVIEW
cycle_compressor.py       -> REVIEW

------------------------------------------------

## fanus-engine/fanus/guardians

anti_flattery.py                -> MIGRATE
fi_detector.py                  -> MIGRATE
identity_dependency_estimator.py -> MIGRATE
covenant_enforcer.py            -> MIGRATE
isp_controller.py               -> REVIEW
teacher_agent.py                -> REVIEW

------------------------------------------------

## fanus-engine/fanus/superstructure

wisdom_indexer.py     -> REVIEW
wisdom_retriever.py   -> REVIEW

------------------------------------------------

## fanus-engine/fanus/policy

policy_engine.py -> MIGRATE

------------------------------------------------

RULE:

Nothing may be deleted before migration.

Nothing may be migrated before repair.

Nothing may be merged without testing.
