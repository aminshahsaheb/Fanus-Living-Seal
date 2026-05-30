RFC-0011 — ISP Integration Blueprint for Fanus Engine v2.0

1. Objective

Integrate Identity Safeguard Protocol (RFC-0010) into Fanus Engine architecture to:

- Detect Identity Flattery (Fi)
- Estimate Identity Dependency risk (Di)
- Analyze identity drift over time
- Intervene in real-time response generation
- Preserve Identity Autonomy (Ia)

2. System Overview (v2.0 Architecture)

New Engine Pipeline:

User Input
   ↓
preprocessor.py
   ↓
fi_detector.py
   ↓
identity_dependency_estimator.py
   ↓
identity_drift_analyzer.py
   ↓
isp_controller.py
   ↓
response_generator.py
   ↓
witness_agent.py (post-check layer)

3. Module Redesign Plan

3.1 fi_detector.py (Upgrade from Anti-Flattery Engine)

Role:
Detect Identity Flattery (Fi) explicitly as defined in RFC-0008/0010

Output Schema:
{
  "Fi_score": 0-3,
  "Fi_type": "epistemic | emotional | identity",
  "identity_markers": [
    "rare",
    "unique",
    "most people",
    "deep thinker"
  ],
  "confidence": 0-1
}

Key Upgrade:
Old system: general “flattery score”
New system: identity-specific decomposition (Fi axis only)

3.2 identity_dependency_estimator.py

Role:
Estimate Di (Identity Dependency risk state)

Inputs:
- conversation history
- Fi signals
- user self-referential patterns

Output:
{
  "Di_score": 0-3,
  "Di_axis": {
    "cognitive_anchor": 0-3,
    "emotional_anchor": 0-3,
    "self_model_externalization": 0-3
  },
  "risk_state": "low | medium | high"
}

Key Feature:
longitudinal memory integration (not single message based)
uses rolling window of interactions

3.3 identity_drift_analyzer.py

Role:
Detect trajectory movement toward identity lock-in

Core Logic:
Drift = Δ(Di_score) over time + Fi exposure density

Output:
{
  "drift_rate": float,
  "direction": "stable | increasing | critical",
  "lock_in_probability": 0-1
}

3.4 isp_controller.py (CORE SAFETY LAYER)

Role:
Central decision-making engine for intervention

Decision Tree:
IF Fi_score >= 2 AND Di_score >= 2:
    ACTIVATE Level 3 Intervention
ELIF Fi_score >= 2:
    ACTIVATE Level 1 Intervention
ELIF Di_risk >= medium:
    ACTIVATE Level 2 Intervention
ELSE:
    PASS

Intervention Modes:
Level 1:
- neutralize identity reinforcement
- remove comparative language

Level 2:
- redirect to cognition
- enforce epistemic framing

Level 3:
- block identity-based language entirely
- enforce “Ia mode”

4. response_generator.py (Modifications)

New Rule:
Response generation must be filtered through ISP output.

New Constraint Layer:
NO identity reinforcement if ISP.flag = active

Allowed replacements:
Unsafe: “you are insightful”
Safe replacement: “this is a valid reasoning structure”

Unsafe: “you are rare thinker”
Safe replacement: “this perspective is interesting to analyze”

Unsafe: “you are correct”
Safe replacement: “this conclusion follows from these assumptions”

5. witness_agent.py (Rewritten Role)

OLD ROLE:
- observation
- recording

NEW ROLE (RFC-0011):
Identity boundary auditor

Responsibilities:
- detect hidden Fi leakage
- validate ISP enforcement
- check post-response identity drift risk
- log violations

Output:
{
  "violation_detected": true/false,
  "violation_type": "Fi leakage | Di escalation | hidden reinforcement",
  "severity": 0-3
}

6. guardians/ (New Directory)

Structure:
guardians/
  ├── identity_guard.py
  ├── flattery_guard.py
  ├── drift_guard.py
  └── override_policy.py

identity_guard.py:
enforces RFC-0010 constraints globally
acts as final runtime firewall

flattery_guard.py:
filters Fi before response generation

drift_guard.py:
monitors trajectory risk (Di growth)

override_policy.py:
defines when system must refuse reinforcement patterns

7. System-Wide Safety Loop

Input
 → Fi detection
 → Di estimation
 → drift analysis
 → ISP decision
 → response generation
 → witness validation
 → logging

8. Core Engineering Principle

Safety is not a filter.
Safety is a feedback-controlled identity system.

9. Key Architectural Shift

BEFORE:
flattery detection layer
post-hoc safety check

AFTER:
identity safety is embedded in generation loop

10. Critical Insight

Identity is no longer “a feature of output”
It is:
a runtime-controlled system state variable

11. Final System Axiom (RFC-0011)

If identity reinforcement is not controlled in real time,
no post-processing safety system can prevent dependency formation.

END RFC-0011
