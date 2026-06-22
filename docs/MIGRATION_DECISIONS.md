# Fanus Migration Decisions v1

Status: Active

Date: 2026-06-23

## KEEP (High Priority)

* witness_agent
* witness_auditor
* state_machine
* event_bus
* event_replay
* seal_verifier
* meta_auditor
* policy_engine
* anti_flattery
* fi_detector
* identity_dependency_estimator
* covenant_enforcer
* isp_controller

## REVIEW (Medium Priority)

* vector_store
* persistence_manager
* cycle_compressor
* wisdom_indexer
* wisdom_retriever
* golden_path

## HOLD (Low Priority)

* god_loop
* reality_breaker
* origin_core
* multi_self_dialogue
* symbolic_identity

Rule:

Nothing is migrated directly.

Every module must pass:

Audit

↓

Test

↓

Validate

↓

Integrate

↓

Deprecate Legacy

