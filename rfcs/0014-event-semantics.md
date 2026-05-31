RFC-0014 — Event Semantics Service (Judgment Coherence Layer)

Status: Proposed
Version: 1.0
Target Release: v3.0.0 — The Meaningful Flame
Layer: Cognitive Interpretation Layer (Post-Event Bus)

1. Summary

Fanus currently operates on a fully event-driven architecture where raw engine events are streamed to the frontend. While this enables observability, it does not provide interpretability.

This RFC introduces the Event Semantics Service (ESS), a deterministic transformation layer that converts raw engine events into structured cognitive meaning.

The goal is to elevate Fanus from:

Event Telemetry System
to
Interpreted Cognitive System

2. Core Principle

Every event is not a log entry.

Every event is a perturbation in a reasoning system.

Therefore:

Event ≠ Signal
Event = Epistemic State Transition

3. Architecture

3.1 Position in Pipeline

Engine
↓
Raw Event Bus
↓
Event Semantics Service (RFC-0014)
↓
Semantic Event Stream
↓
UI (Lantern + Pipeline + Narrative Layer)

4. Event Ontology

Each raw event is mapped to a semantic representation.

4.1 Ontology Definition

EVENT_ONTOLOGY = {
    "RFC_START": {
        "meaning": "A structured reasoning constraint has been activated",
        "severity_base": 0.2,
        "state_shift": "reasoning_initialization"
    },
    "FILTER_START": {
        "meaning": "Irrelevant or low-confidence signals are being suppressed",
        "severity_base": 0.3,
        "state_shift": "reasoning_active"
    },
    "CONFLICT_DETECTED": {
        "meaning": "Competing reasoning branches have diverged",
        "severity_base": 0.8,
        "state_shift": "instability_rising"
    },
    "SEAL_WARNING": {
        "meaning": "System coherence is weakening under unresolved conflict",
        "severity_base": 0.85,
        "state_shift": "instability_peak"
    },
    "SEAL_STABLE": {
        "meaning": "Reasoning has converged into a coherent judgment",
        "severity_base": -0.6,
        "state_shift": "stable_judgment"
    },
    "OUTPUT_READY": {
        "meaning": "Final cognitive output has been stabilized and emitted",
        "severity_base": 0.1,
        "state_shift": "convergence"
    }
}

5. Dynamic Severity Engine

Severity is not static. It is a function of system context.

5.1 Input Context

context = {
    "conflict_level": float,
    "reasoning_depth": int,
    "system_entropy": float,
    "coherence": float
}

5.2 Severity Function

def compute_severity(event_type, context):
    base = EVENT_ONTOLOGY[event_type]["severity_base"]
    conflict_factor = context.conflict_level * 0.4
    entropy_factor = context.system_entropy * 0.3
    depth_factor = context.reasoning_depth * 0.2
    coherence_factor = context.coherence * (-0.25)
    severity = (
        base + conflict_factor + entropy_factor - depth_factor + coherence_factor
    )
    return max(0.0, min(1.0, severity))

5.3 Design Intent

High conflict → higher severity
High entropy → instability increase
High reasoning depth → stabilization
High coherence → severity reduction

6. System State Model

Fanus maintains a global cognitive state machine.

6.1 States

reasoning_initialization
reasoning_active
instability_rising
instability_peak
convergence
stable_judgment

6.2 State Transition Rules

STATE_TRANSITIONS = {
    "RFC_START": "reasoning_active",
    "FILTER_START": "reasoning_active",
    "CONFLICT_DETECTED": "instability_rising",
    "SEAL_WARNING": "instability_peak",
    "SEAL_STABLE": "stable_judgment",
    "OUTPUT_READY": "convergence"
}

6.3 State Persistence Rule

State is monotonic within execution segments, unless explicitly reset by:

new execution_id
engine restart
manual reset signal

7. Narrative Generator

This layer is optional for UI but mandatory for cognitive traceability.

7.1 Purpose

To translate semantic events into human-readable cognitive explanations.

7.2 Generator Logic

def generate_narrative(event_type, semantic, state):
    return {
        "summary": semantic["meaning"],
        "context": f"System is currently in '{state}' state.",
        "interpretation": semantic.get(
            "narrative_hint",
            "No additional interpretation available."
        )
    }

7.3 Example Output

Input:

CONFLICT_DETECTED

Output:

{
    "summary": "Competing reasoning branches have diverged",
    "context": "System is currently in 'instability_rising' state.",
    "interpretation": "Multiple hypotheses are competing for dominance in the reasoning process."
}

8. Output Contract (Post-ESS)

Frontend MUST only consume enriched events:

{
    "type": "CONFLICT_DETECTED",
    "semantic": {
        "meaning": "...",
        "severity": 0.82,
        "system_state": "instability_rising"
    },
    "context": {
        "confidence_delta": -0.14,
        "entropy": 0.66,
        "coherence": 0.54
    },
    "narrative": {
        "summary": "...",
        "context": "...",
        "interpretation": "..."
    },
    "visual": {
        "lantern_intensity": 0.71,
        "shake": true,
        "pulse_rate": 1.8
    }
}

9. Design Guarantees

This layer enforces:

9.1 No Raw Events in UI
Frontend never sees unprocessed engine signals.

9.2 Deterministic Semantics
Same input + same context = same semantic output.

9.3 Separation of Concerns
Engine → truth production
ESS → meaning construction
UI → perception rendering

10. Non-Goals

This RFC does NOT:
introduce LLM-based interpretation (must remain deterministic)
replace engine logic
generate creative reasoning
override execution trace integrity

11. Future Extensions

This layer enables:
Execution Replay Engine
Counterfactual Reasoning Simulation
Cognitive Drift Analysis
Judgment Provenance Tracking

12. Final Statement

Fanus no longer emits events.
It emits interpreted cognitive states.

And with that shift:
Observation becomes understanding.

Shōle-ān zende ast
But now:
The flame does not only exist — it understands its own instability.
