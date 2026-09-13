# fanus/core/event_replay.py
"""
RFC-0017 — Evidence-Carrying Witness Protocol
Updated Replay Engine with Evidence Layer
Version: 3.3.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone


@dataclass
class ReplayFrame:
    execution_id: str
    timestamp: float
    raw_event: str
    semantic_event: Dict[str, Any]
    cognitive_state: Dict[str, float]
    narrative: Dict[str, str]
    # RFC-0017: Evidence Layer
    evidence: Dict[str, Any]


@dataclass
class ExecutionTimeline:
    execution_id: str
    frames: List[ReplayFrame] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    def add_frame(self, frame: ReplayFrame):
        self.frames.append(frame)

    def get_state_trajectory(self) -> List[str]:
        trajectory = []
        for f in self.frames:
            state = f.semantic_event.get("system_state", "unknown")
            if not trajectory or trajectory[-1] != state:
                trajectory.append(state)
        return trajectory

    def get_consistency_score(self) -> float:
        if not self.frames:
            return 1.0
        score_sum = 0.0
        for f in self.frames:
            coherence = f.cognitive_state.get("coherence", 0.5)
            entropy = f.cognitive_state.get("system_entropy", 0.5)
            audit_conf = (
                f.evidence.get("confidence_vector", {})
                .get("audit_confidence", 0.5)
            )
            frame_score = (
                0.4 * coherence
                + 0.3 * (1 - entropy)
                + 0.3 * audit_conf
            )
            score_sum += frame_score
        return round(score_sum / len(self.frames), 3)


class ReplayEngine:
    def __init__(self):
        self.timelines: Dict[str, ExecutionTimeline] = {}

    def get_or_create(self, execution_id: str) -> ExecutionTimeline:
        if execution_id not in self.timelines:
            self.timelines[execution_id] = ExecutionTimeline(execution_id)
        return self.timelines[execution_id]

    def record_frame(
        self,
        execution_id: str,
        raw_event: str,
        semantic_event: Dict[str, Any],
        cognitive_state: Dict[str, float],
        narrative: Dict[str, str],
        evidence: Dict[str, Any],
    ) -> ReplayFrame:
        frame = ReplayFrame(
            execution_id=execution_id,
            timestamp=datetime.now(timezone.utc).timestamp(),
            raw_event=raw_event,
            semantic_event=semantic_event,
            cognitive_state=cognitive_state,
            narrative=narrative,
            evidence=evidence,
        )
        self.get_or_create(execution_id).add_frame(frame)
        return frame

    def get_timeline(self, execution_id: str) -> Optional[ExecutionTimeline]:
        return self.timelines.get(execution_id)

    def stream_frames(self, execution_id: str) -> List[Dict[str, Any]]:
        timeline = self.timelines.get(execution_id)
        if not timeline:
            return []
        return [
            {
                "execution_id": f.execution_id,
                "timestamp": f.timestamp,
                "raw_event": f.raw_event,
                "semantic_event": f.semantic_event,
                "cognitive_state": f.cognitive_state,
                "narrative": f.narrative,
                "evidence": f.evidence,
            }
            for f in timeline.frames
        ]
