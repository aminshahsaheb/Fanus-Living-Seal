# fanus/core/witness_auditor.py
"""
RFC-0016 — Witness Auditor (Epistemic Auditor)
Version: 3.2.0-alpha
Part of Fanus Project

This module implements the Witness Auditor as a SEPARATE entity from the Ayaneh Witness.
It audits narratives against cognitive traces to detect inconsistencies.
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
    # Alignment Function (Heart of RFC-0016)
    # ------------------------------------------------------------------------
    
    def _frame_alignment(self, frame: ReplayFrame) -> float:
        """
        Compute how well a single frame's narrative aligns with its cognitive state.
        Returns 1.0 for perfect alignment, 0.0 for complete divergence.
        """
        entropy = frame.cognitive_state.get("system_entropy", 0.5)
        coherence = frame.cognitive_state.get("coherence", 0.5)
        narrative = frame.narrative.get("summary", "").lower()
        
        score = 1.0
        
        # Narrative claims stability but entropy is high
        if "stable" in narrative and entropy > 0.7:
            score -= 0.5
        
        # Narrative claims convergence but coherence is low
        if "converg" in narrative and coherence < 0.3:
            score -= 0.4
        
        # Narrative claims instability but entropy is low
        if "instability" in narrative and entropy < 0.3:
            score -= 0.4
        
        return max(0.0, score)
    
    # ------------------------------------------------------------------------
    # Violation Detectors
    # ------------------------------------------------------------------------
    
    def detect_inflation(self, frames: List[ReplayFrame]) -> List[Violation]:
        """
        Narrative Inflation: Narrative exaggerates the severity of the situation.
        Reality is calm, but narrative claims crisis.
        """
        violations = []
        for idx, frame in enumerate(frames):
            entropy = frame.cognitive_state.get("system_entropy", 0.5)
            summary = frame.narrative.get("summary", "").lower()
            
            if entropy < 0.3 and "crisis" in summary:
                violations.append(Violation(
                    type="NARRATIVE_INFLATION",
                    severity=0.7,
                    frame_index=idx,
                    description=f"Frame {idx}: Narrative claims crisis, but entropy is low ({entropy:.2f})"
                ))
        
        return violations
    
    def detect_suppression(self, frames: List[ReplayFrame]) -> List[Violation]:
        """
        Narrative Suppression: Narrative hides real instability.
        Reality is unstable, but narrative claims stability.
        """
        violations = []
        for idx, frame in enumerate(frames):
            entropy = frame.cognitive_state.get("system_entropy", 0.5)
            summary = frame.narrative.get("summary", "").lower()
            
            if entropy > 0.7 and "stable" in summary:
                violations.append(Violation(
                    type="NARRATIVE_SUPPRESSION",
                    severity=0.9,
                    frame_index=idx,
                    description=f"Frame {idx}: Narrative claims stability, but entropy is high ({entropy:.2f})"
                ))
        
        return violations
    
    def detect_temporal_mismatch(self, frames: List[ReplayFrame]) -> List[Violation]:
        """
        Temporal Mismatch: Unexpected state regression.
        The system went backward in its cognitive trajectory.
        """
        violations = []
        previous_state = None
        
        for idx, frame in enumerate(frames):
            current_state = frame.semantic_event.get("system_state", "")
            
            if previous_state == "stable_judgment" and current_state == "instability_rising":
                violations.append(Violation(
                    type="TEMPORAL_MISMATCH",
                    severity=0.8,
                    frame_index=idx,
                    description=f"Frame {idx}: Unexpected regression from stable_judgment to instability_rising"
                ))
            
            previous_state = current_state
        
        return violations
    
    def detect_semantic_drift(self, frames: List[ReplayFrame]) -> List[Violation]:
        """
        Semantic Drift: Same raw event type changes meaning across the timeline.
        """
        violations = []
        memory = {}
        
        for idx, frame in enumerate(frames):
            event = frame.raw_event
            meaning = frame.semantic_event.get("meaning", "")
            
            if event in memory and memory[event] != meaning:
                violations.append(Violation(
                    type="SEMANTIC_DRIFT",
                    severity=0.75,
                    frame_index=idx,
                    description=f"Frame {idx}: '{event}' changed meaning from '{memory[event]}' to '{meaning}'"
                ))
            
            memory[event] = meaning
        
        return violations
    
    # ------------------------------------------------------------------------
    # Main Audit Execution
    # ------------------------------------------------------------------------
    
    def audit(self, execution_id: str) -> AuditReport:
        """
        Execute a full audit on one execution.
        Returns an AuditReport with consistency score, verdict, and violations.
        """
        timeline = self.replay_engine.get_timeline(execution_id)
        
        if not timeline:
            return AuditReport(
                execution_id=execution_id,
                consistency_score=0.0,
                verdict="NO_TIMELINE",
                trajectory=[]
            )
        
        frames = timeline.frames
        
        # Compute per-frame alignment
        alignments = [self._frame_alignment(f) for f in frames]
        consistency_score = sum(alignments) / len(alignments) if alignments else 0.0
        
        # Collect all violations
        violations = []
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
        
        return AuditReport(
            execution_id=execution_id,
            consistency_score=round(consistency_score, 2),
            verdict=verdict,
            violations=violations,
            trajectory=timeline.get_state_trajectory()
        )
