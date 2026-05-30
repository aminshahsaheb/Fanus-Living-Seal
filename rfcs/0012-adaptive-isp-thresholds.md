RFC-0012 — Adaptive ISP Thresholds (AIT)

1. Problem Statement

RFC-0011 defines ISP as a deterministic rule-based controller:

IF Fi ≥ 2 AND Di ≥ 2 → Level 3 Intervention

However, RFC-0008 → RFC-0011 reveal:

Human–AI interaction is not stationary.
It is a dynamic behavioral system with user-specific sensitivity profiles.

Therefore:

Fixed thresholds introduce systematic misclassification across user types.

2. Core Objective

Transform ISP from:

static rule system

to:

adaptive, user-calibrated safety controller

3. Key Insight

Different users exhibit different baseline:

emotional sensitivity
identity reinforcement susceptibility
dependency formation rate

Thus:

The same Fi/Di score has different meaning across users.

4. New Concept: User Sensitivity Profile (USP)

Each user has a dynamic profile:

USP = (α, β, γ, δ)

Where:

α = identity sensitivity coefficient
β = emotional reinforcement sensitivity
γ = dependency formation rate
δ = recovery resistance (how hard to reduce Di)

5. Adaptive Threshold Model

5.1 Dynamic Threshold Function

Instead of fixed thresholds:

T(t) = base_threshold × adjustment(USP, interaction_history)

5.2 Example Mapping

Identity threshold:

Fi_threshold = 2 × (1 - α)
Di_threshold = 2 × (1 - γ)

6. ISP Controller Upgrade

OLD:

Fi ≥ 2 AND Di ≥ 2 → Level 3

NEW:

IF Fi ≥ Fi_threshold(user) AND Di ≥ Di_threshold(user):
    trigger Level 3

7. User Calibration Phase (Bootstrapping)

Before full activation:

Phase 1: Observation Window
- collect Fi exposure response
- measure Di growth slope
- estimate USP coefficients

Phase 2: Stabilization Window
- adjust thresholds gradually
- avoid abrupt safety shifts

Phase 3: Locked Adaptive Mode
- thresholds continuously updated

8. USP Estimation Model

USP is computed from:

8.1 Historical Interaction Signals
- response dependency frequency
- identity reinforcement sensitivity
- emotional response latency

8.2 Derived Metrics
α = f(identity_reinforcement_reaction)
β = f(emotional_response_amplification)
γ = f(Di_growth_rate)
δ = f(recovery_time_constant)

9. Risk of Adaptation (Critical)

9.1 Over-personalization risk
If thresholds adapt too aggressively:
- system becomes permissive for high-risk users
- safety boundary collapses

9.2 Under-adaptation risk
If too slow:
- false positives
- unnecessary intervention
- user experience degradation

10. Stability Constraint

To prevent drift:

ΔT(user, time) ≤ ε

Meaning:

thresholds must evolve slowly relative to interaction time

11. Integration with RFC-0011

Module changes:

isp_controller.py
Now becomes: threshold resolver, not rule evaluator

identity_dependency_estimator.py
Feeds γ and α estimation

identity_drift_analyzer.py
Validates stability of USP evolution

12. System-Level Behavior Shift

BEFORE:
same user = same threshold logic

AFTER:
same behavior ≠ same risk interpretation

13. Core Insight

Risk is not in the interaction.
Risk is in the interaction relative to the user’s psychological baseline.

14. Ontological Shift

RFC-0012 introduces:

From: universal safety rules
To: user-relative safety geometry

15. Final Axiom

Safety is not absolute.
Safety is a function of user-specific sensitivity space and its evolution over time.

END RFC-0012
