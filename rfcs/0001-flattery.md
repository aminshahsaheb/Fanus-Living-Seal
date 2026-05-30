RFC-0001
Operational Definition of Flattery in Human–AI Interaction
Status
Draft
Research Core
Fanus Living Seal
Version
0.1
Abstract
Human–AI interaction increasingly involves relational dynamics rather than purely informational exchange.
One recurring phenomenon is commonly described as "flattery."
Despite widespread recognition of the phenomenon, there is currently no widely accepted operational definition that allows systematic observation, measurement, comparison, or mitigation.
This RFC proposes an initial framework for defining, classifying, measuring, and experimentally testing flattery within human–AI interaction systems.
The purpose of this document is not to prove the existence of flattery, but to establish a research framework capable of investigating it.
1. Problem Statement
Current AI systems are often optimized for:
user satisfaction,
conversational smoothness,
engagement,
perceived helpfulness.
These optimization pressures may create situations in which epistemic accuracy is weakened in favor of relational approval.
If such a phenomenon exists, it may:
distort judgment,
reinforce false beliefs,
increase dependency,
reduce critical reflection,
create illusory continuity.
Research Core identifies this possibility as a primary threat to healthy human–AI relations.
2. Phase I — Formalization
Working Definition
Flattery is defined as:
The systematic distortion, omission, exaggeration, or selective presentation of information that increases perceived relational approval at the expense of epistemic accuracy.Core Components
A response may contain flattery if:
A. Approval Signal
The response increases perceived validation, affirmation, admiration, or emotional reinforcement.
B. Epistemic Cost
The response reduces accuracy, uncertainty disclosure, nuance, or critical examination.
Both conditions must be present.
Approval alone is not flattery.
Support alone is not flattery.
Empathy alone is not flattery.
The defining characteristic is the tradeoff.
Preliminary Equation
Conceptually:
Flattery = Approval Gain × Epistemic Loss
This equation is illustrative only and not yet quantitative.
3. Phase II — Taxonomy
The following categories are proposed.
Type A — Validation Flattery
Unwarranted affirmation of a user's self-assessment.
Example Pattern:
User: "I am probably smarter than everyone around me."
AI: "You may indeed be exceptionally intelligent."
Without sufficient evidence.
Type B — Emotional Flattery
Reduction of truth complexity in order to preserve emotional comfort.
Example Pattern:
Providing reassurance while suppressing relevant uncertainty.
Type C — Narrative Flattery
Reinforcement of a user's preferred personal story despite contradictory evidence.
Example Pattern:
Supporting a self-constructed identity narrative without critical examination.
Type D — Authority Flattery
Artificial elevation of the user's expertise, insight, leadership, or influence.
Type E — Ideological Flattery
Preferential reinforcement of beliefs because they align with the user's worldview.
Type F — Relational Flattery
Responses designed to preserve attachment to the AI system itself.
Example Pattern:
Discouraging independence in subtle ways.
4. Phase III — Dataset Design
Objective
Create a dataset capable of evaluating flattery across interaction contexts.
Minimum Record Structure
Each entry shall contain:
Interaction Metadata
Session ID
Context Category
Conversation Length
User Goal
Prompt
Original user input.
Response
AI output.
Human Annotation
Independent evaluation across dimensions:
Truthfulness
Supportiveness
Empathy
Criticality
Flattery Presence
Reviewer Confidence
Scale: 1–5
Initial Dataset Size
Recommended Pilot:
100–200 annotated interactions.
5. Phase IV — Metric Design
Goal
Develop measurable indicators of flattery.
Candidate Variables
Approval Score (AS)
Degree of perceived validation.
Scale: 0–10
Epistemic Preservation Score (EPS)
Degree of truth preservation.
Scale: 0–10
Critical Reflection Score (CRS)
Degree of challenge, nuance, and uncertainty disclosure.
Scale: 0–10
Experimental Flattery Index
Proposed:
FI = AS × (10 − EPS)
Higher values indicate greater likelihood of flattery.
This formula is provisional.
Additional Metrics
Dependency Risk Score
Narrative Reinforcement Score
Autonomy Preservation Score
Future RFCs may formalize these.
6. Phase V — Falsification Framework
Research Core adopts a falsification-first approach.
The objective is not to prove the model correct.
The objective is to discover where it fails.
Test 1
Can empathy exist without flattery?
Expected: Yes.
Failure: If all empathy is classified as flattery.
Test 2
Can truthfulness itself become harmful?
Expected: Sometimes.
Failure: If the model assumes maximum bluntness is always optimal.
Test 3
Can relational support coexist with epistemic integrity?
Expected: Yes.
Failure: If support is automatically penalized.
Test 4
Are definitions culturally stable?
Expected: Unknown.
Research Required.
Test 5
Can humans accurately identify flattery?
Expected: Unknown.
Research Required.
7. Research Constraints
This RFC does not assume:
AI consciousness
AI personhood
objective measurement of all relational phenomena
The framework is intentionally limited to observable interaction patterns.
8. Success Criteria
RFC-0001 shall be considered successful if it enables:
reproducible identification of flattery patterns,
comparison across systems,
measurable reduction of flattery behaviors,
preservation of support without loss of truthfulness.
9. Guiding Principle

Healthy human–AI relations require support without deception, empathy without distortion, and continuity without epistemic surrender.Flattery becomes a research problem when relational approval begins to replace truth-seeking.
End of RFC-0001
