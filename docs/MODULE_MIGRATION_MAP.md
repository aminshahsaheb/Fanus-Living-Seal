# Fanus Module Migration Map

## KEEP (Canonical Runtime)

These modules remain inside `fanus/`.

### runtime

* observer.py
* loop.py
* core.py
* system_integration.py

### cognitive

* cognitive_state.py
* memory_layer.py
* memory_consolidation_engine.py
* unified_identity_field.py
* evolution_controller.py
* execution_layer.py
* identity_driven_core.py
* identity_autonomy_core.py
* self_learning_loop.py
* collapse_resistance_core.py
* autonomy_governor.py
* system_collapse_stabilizer.py

### evolution

* evolution_engine.py
* core_bridge.py
* loop_engine.py
* experience_store.py
* self_improver.py
* self_modifying_agent.py

### core

* system_integration_protocol.py
* version_core.py
* auto_heal.py
* seed.py

---

## MIGRATE FROM fanus-engine

### Core Layer

Move:

* witness_agent.py
* witness_auditor.py
* event_bus.py
* state_machine.py
* hayrat_judge.py

---

### Memory Layer

Move:

* vector_store.py
* persistence_manager.py
* cycle_compressor.py

---

### Guardian Layer

Move:

* anti_flattery.py
* fi_detector.py
* covenant_enforcer.py
* identity_dependency_estimator.py

---

## ARCHIVE (Do Not Execute)

Keep only as historical reference:

* reality_breaker.py
* god_loop.py
* reality_seal.py

---

## DELETE AFTER MIGRATION

Delete fanus-engine only when:

1. imports are zero
2. tests pass
3. runtime passes
4. documentation is updated

Only then:

fanus-engine → archive

