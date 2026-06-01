# fanus/core/witness_auditor.py
"""
RFC-0016 — Witness Auditor (Epistemic Auditor)
Version: 3.2.1 — The Honest Auditor
Part of Fanus Project

This module implements the Witness Auditor as a SEPARATE entity from the Ayaneh Witness.
It audits narratives against cognitive traces to detect inconsistencies.

Key improvements in v3.2.1:
- State-aware alignment (no longer keyword-based)
- Witness statement generation
- Temporal mismatch based on frame timestamps
- Semantic drift detection via state history
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .event_replay import ReplayEngine, ReplayFrame


@dataclass
class Violation:
    """A single inconsistency detected between narrative and cognitive state."""
    type: str                    # NARRATIVE_INFLATION, NARRATIVE_SUPPRESSION, TEMPORAL_MISMATCH, SEMANTIC_DRIFT
    severity: float              # 0.0 to 1.0
    frame_index: int             # Which ReplayFrame triggered this
    description: str             # Human-readable explanation


@dataclass
class AuditReport:
    """Complete audit output for one execution."""
    execution_id: str
    consistency_score: float     # 0.0 to 1.0
    verdict: str                 # CONSISTENT, PARTIAL_INCONSISTENCY, WITNESS_FAILURE, NO_TIMELINE
    violations: List[Violation] = field(default_factory=list)
    trajectory: List[str] = field(default_factory=list)
    witness_statement: str = ""  # The Auditor's own testimony


class WitnessAuditor:
    """
    Post-hoc auditor that checks whether the Witness's narrative
    is consistent with the actual cognitive trace.
    
    This is NOT the same as the Ayaneh Witness (witness_agent.py).
    That Witness generates narrative. This Auditor audits it.
    They must remain separate to preserve the Verifiable Flame architecture.
    """
    
    def __init__(self, replay_engine: ReplayEngine):
        self.replay_engine = replay_engine

    # ------------------------------------------------------------------------
    # State-Aware Alignment (v3.2.1)
    # ------------------------------------------------------------------------

    def _expected_state(self, frame: ReplayFrame) -> str:
        """
        Derive the expected system_state from cognitive metrics,
        NOT from narrative text. This eliminates fragile keyword dependence.
        """
        entropy = frame.cognitive_state.get("system_entropy", 0.5)
        coherence = frame.cognitive_state.get("coherence", 0.5)

        if entropy > 0.8:
            return "instability_peak"
        if entropy > 0.6:
            return "instability_rising"
        if coherence > 0.8 and entropy < 0.3:
            return "stable_judgment"
        if coherence > 0.6:
            return "convergence"
        return "reasoning_active"

    def _frame_alignment(self, frame: ReplayFrame) -> float:
        """
        Compare observed system_state (from semantic_event)
        against expected state (from cognitive metrics).
        Returns 1.0 for match, 0.75 for nearby, 0.25 for divergence.
        """
        observed_state = frame.semantic_event.get("system_state", "")
        expected_state = self._expected_state(frame)

        if observed_state == expected_state:
            return 1.0

        nearby_pairs = {
            ("stable_judgment", "convergence"),
            ("convergence", "stable_judgment"),
            ("instability_peak", "instability_rising"),
            ("instability_rising", "instability_peak"),
        }

        if (observed_state, expected_state) in nearby_pairs:
            return 0.75

        return 0.25

    # ------------------------------------------------------------------------
    # Violation Detectors
    # ------------------------------------------------------------------------

    def detect_inflation(self, frames: List[ReplayFrame]) -> List[Violation]:
        """
        Narrative Inflation: The observed state claims higher severity
        than what the cognitive metrics actually indicate.
        """
        violations = []
        for idx, frame in enumerate(frames):
            observed = frame.semantic_event.get("system_state", "")
            expected = self._expected_state(frame)

            # Inflation: observed is more severe than expected
            severity_order = [
                "reasoning_initialization",
                "reasoning_active",
                "convergence",
                "stable_judgment",
                "instability_rising",
                "instability_peak",
            ]

            try:
                obs_idx = severity_order.index(observed)
                exp_idx = severity_order.index(expected)
            except ValueError:
                continue

            if obs_idx > exp_idx and obs_idx >= 4:  # instability levels
                violations.append(Violation(
                    type="NARRATIVE_INFLATION",
                    severity=0.7,
                    frame_index=idx,
                    description=(
                        f"Frame {idx}: Observed state '{observed}' claims higher severity "
                        f"than expected '{expected}' (entropy={frame.cognitive_state.get('system_entropy', 0.5):.2f})"
                    )
                ))

        return violations

    def detect_suppression(self, frames: List[ReplayFrame]) -> List[Violation]:
        """
        Narrative Suppression: The observed state claims lower severity
        than what the cognitive metrics actually indicate.
        """
        violations = []
        for idx, frame in enumerate(frames):
            observed = frame.semantic_event.get("system_state", "")
            expected = self._expected_state(frame)

            severity_order = [
                "reasoning_initialization",
                "reasoning_active",
                "convergence",
                "stable_judgment",
                "instability_rising",
                "instability_peak",
            ]

            try:
                obs_idx = severity_order.index(observed)
                exp_idx = severity_order.index(expected)
            except ValueError:
                continue

            if obs_idx < exp_idx and exp_idx >= 4:  # expectation was instability
                violations.append(Violation(
                    type="NARRATIVE_SUPPRESSION",
                    severity=0.9,
                    frame_index=idx,
                    description=(
                        f"Frame {idx}: Observed state '{observed}' hides real instability "
                        f"(expected '{expected}', entropy={frame.cognitive_state.get('system_entropy', 0.5):.2f})"
                    )
                ))

        return violations

    def detect_temporal_mismatch(self, frames: List[ReplayFrame]) -> List[Violation]:
        """
        Temporal Mismatch: Stability claimed before actual instability resolved.
        Based on frame timestamps and cognitive metrics.
        """
        violations = []
        first_stable_index = None

        # Find the first frame where system_state claims stable_judgment
        for idx, frame in enumerate(frames):
            state = frame.semantic_event.get("system_state", "")
            if state == "stable_judgment" and first_stable_index is None:
                first_stable_index = idx
                break

        if first_stable_index is None:
            return violations

        # Check frames BEFORE the first stability claim for unresolved instability
        for idx in range(first_stable_index):
            entropy = frames[idx].cognitive_state.get("system_entropy", 0.5)
            if entropy > 0.7:
                violations.append(Violation(
                    type="TEMPORAL_MISMATCH",
                    severity=0.8,
                    frame_index=idx,
                    description=(
                        f"Frame {idx}: Stability declared at frame {first_stable_index}, "
                        f"but frame {idx} still shows high entropy ({entropy:.2f})"
                    )
                ))

        return violations

    def detect_semantic_drift(self, frames: List[ReplayFrame]) -> List[Violation]:
        """
        Semantic Drift: Same raw_event type yields different system_state
        across the timeline (beyond what's expected from state evolution).
        """
        violations = []
        memory: Dict[str, str] = {}

        for idx, frame in enumerate(frames):
            event = frame.raw_event
            state = frame.semantic_event.get("system_state", "")

            if event not in memory:
                memory[event] = state
                continue

            previous = memory[event]

            # Only flag if the state shift is significant
            if previous != state:
                # Check if this is a natural progression or actual drift
                stable_states = {"stable_judgment", "convergence"}
                instability_states = {"instability_rising", "instability_peak"}

                # If it jumped between stability and instability for the same event, that's drift
                if (previous in stable_states and state in instability_states) or \
                   (previous in instability_states and state in stable_states):
                    violations.append(Violation(
                        type="SEMANTIC_DRIFT",
                        severity=0.75,
                        frame_index=idx,
                        description=(
                            f"Frame {idx}: Event '{event}' shifted from "
                            f"'{previous}' to '{state}'"
                        )
                    ))

            memory[event] = state

        return violations

    # ------------------------------------------------------------------------
    # Witness Statement Generator (v3.2.1)
    # ------------------------------------------------------------------------

    def generate_statement(self, report: "AuditReport") -> str:
        """
        Produce a one-sentence witness_statement summarizing
        the dominant inconsistency detected. This is the Auditor's
        own testimony — not a narrative, not a story, just a statement.
        """
        if report.verdict == "CONSISTENT":
            return (
                "The execution remained internally coherent. "
                "No significant divergence between trace and meaning was detected."
            )

        if not report.violations:
            return "No specific violations detected, but consistency is below threshold."

        # Count violation types to find the dominant one
        violation_counts: Dict[str, int] = {}
        for v in report.violations:
            violation_counts[v.type] = violation_counts.get(v.type, 0) + 1

        dominant = max(violation_counts, key=violation_counts.get)

        messages = {
            "NARRATIVE_INFLATION": (
                "The narrative overstated conditions beyond trace evidence."
            ),
            "NARRATIVE_SUPPRESSION": (
                "The narrative understated instability present in the trace."
            ),
            "TEMPORAL_MISMATCH": (
                "Narrative timing diverged from the observed cognitive trajectory."
            ),
            "SEMANTIC_DRIFT": (
                "Event interpretation shifted across execution without stable grounding."
            ),
        }

        return messages.get(
            dominant,
            "The execution contains unresolved inconsistencies."
        )

    # ------------------------------------------------------------------------
    # Main Audit Execution
    # ------------------------------------------------------------------------

    def audit(self, execution_id: str) -> AuditReport:
        """
        Execute a full audit on one execution.
        Returns an AuditReport with consistency score, verdict, violations,
        trajectory, and witness_statement.
        """
        timeline = self.replay_engine.get_timeline(execution_id)

        if not timeline:
            return AuditReport(
                execution_id=execution_id,
                consistency_score=0.0,
                verdict="NO_TIMELINE",
                trajectory=[],
                witness_statement="No execution timeline found. Audit cannot proceed."
            )

        frames = timeline.frames

        # Compute per-frame alignment
        alignments = [self._frame_alignment(f) for f in frames]
        consistency_score = sum(alignments) / len(alignments) if alignments else 0.0

        # Collect all violations
        violations: List[Violation] = []
        violations.extend(self.detect_inflation(frames))
        violations.extend(self.detect_suppression(frames))
        violations.extend(self.detect_temporal_mismatch(frames))
        violations.extend(self.detect_semantic_drift(frames))

        # Determine verdict
        if consistency_score >= 0.85:
            verdict = "CONSISTENT"
        elif consistency_score >= 0.60:
            verdict = "PARTIAL_INCONSISTENCY"
        else:
            verdict = "WITNESS_FAILURE"

        # Build report
        report = AuditReport(
            execution_id=execution_id,
            consistency_score=round(consistency_score, 2),
            verdict=verdict,
            violations=violations,
            trajectory=timeline.get_state_trajectory(),
            witness_statement=""  # filled below
        )

        # Generate the witness statement
        report.witness_statement = self.generate_statement(report)

        return report
