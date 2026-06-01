# fanus/core/meta_auditor.py
"""
RFC-0017 Extension — Meta-Audit Layer
Version: 1.0

This layer audits the Auditor using Evidence as ground truth.
It prevents Audit Inflation and recursive epistemic dominance.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class MetaAuditReport:
    execution_id: str
    auditor_verdict: str
    evidence_alignment_score: float
    meta_verdict: str
    conflicts: List[str]


class MetaAuditor:
    """
    The system that audits the Witness Auditor.
    """

    def __init__(self, replay_engine):
        self.replay_engine = replay_engine

    def _compare_audit_with_evidence(self, frame) -> float:
        audit_conf = frame.cognitive_state.get("audit_confidence", 0.5)
        evidence_conf = (
            frame.evidence.get("confidence_vector", {})
            .get("generation_confidence", 0.5)
        )
        return 1.0 - abs(audit_conf - evidence_conf)

    def audit(self, execution_id: str) -> MetaAuditReport:
        timeline = self.replay_engine.get_timeline(execution_id)
        if not timeline:
            return MetaAuditReport(
                execution_id=execution_id,
                auditor_verdict="NO_DATA",
                evidence_alignment_score=0.0,
                meta_verdict="INVALID",
                conflicts=["No execution timeline found"]
            )

        frames = timeline.frames
        alignment_scores = []
        conflicts = []

        for i, f in enumerate(frames):
            score = self._compare_audit_with_evidence(f)
            alignment_scores.append(score)
            if score < 0.5:
                conflicts.append(
                    f"Frame {i}: audit diverges from evidence"
                )

        avg_alignment = (
            sum(alignment_scores) / len(alignment_scores)
            if alignment_scores else 0.0
        )

        if avg_alignment > 0.8:
            meta = "AUDIT_VALIDATED"
        elif avg_alignment > 0.6:
            meta = "AUDIT_TENSION"
        elif avg_alignment > 0.4:
            meta = "AUDIT_OVERREACH"
        else:
            meta = "AUDIT_UNTRUSTED"

        return MetaAuditReport(
            execution_id=execution_id,
            auditor_verdict="COMPLETED",
            evidence_alignment_score=round(avg_alignment, 3),
            meta_verdict=meta,
            conflicts=conflicts,
        )
