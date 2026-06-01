# fanus/core/event_replay.py
"""
RFC-0015 — Event Replay Protocol (ERP)
Version: 1.0
Part of Fanus Project

This module provides a replay engine for verifying the consistency
between semantic narratives and actual cognitive states.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone


@dataclass
class ReplayFrame:
    """A single snapshot of cognitive state at a moment in time."""
    execution_id: str
    timestamp: float
    raw_event: str
    semantic_event: Dict[str, Any]
    cognitive_state: Dict[str, float]
    narrative: Dict[str, str]


@dataclass
class ExecutionTimeline:
    """A complete trajectory of cognitive states for one execution."""
    execution_id: str
    frames: List[ReplayFrame] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'))
    
    def add_frame(self, frame: ReplayFrame):
        self.frames.append(frame)
    
    def get_state_trajectory(self) -> List[str]:
        """Extract the sequence of cognitive states."""
        states = []
        for frame in self.frames:
            state = frame.semantic_event.get("system_state", "unknown")
            if not states or states[-1] != state:
                states.append(state)
        return states
    
    def get_consistency_score(self) -> float:
        """Verify how consistent the narratives are with actual cognitive states."""
        if not self.frames:
            return 1.0
        
        consistent_count = 0
        for frame in self.frames:
            state = frame.cognitive_state
            narrative = frame.narrative.get("summary", "")
            
            # Heuristic checks
            coherence = state.get("coherence", 0.5)
            entropy = state.get("system_entropy", 0.5)
            
            # If narrative claims stability but entropy is high, that's a mismatch
            if "stable" in narrative.lower() and entropy > 0.7:
                continue  # Inconsistent
            if "converg" in narrative.lower() and coherence < 0.3:
                continue  # Inconsistent
            if "instability" in narrative.lower() and entropy < 0.3:
                continue  # Inconsistent
            
            consistent_count += 1
        
        return round(consistent_count / len(self.frames), 2)


class ReplayEngine:
    """
    Stores and replays execution timelines.
    Provides narrative verification capabilities.
    """
    
    def __init__(self):
        self.timelines: Dict[str, ExecutionTimeline] = {}
    
    def get_or_create_timeline(self, execution_id: str) -> ExecutionTimeline:
        if execution_id not in self.timelines:
            self.timelines[execution_id] = ExecutionTimeline(execution_id=execution_id)
        return self.timelines[execution_id]
    
    def record_frame(self, execution_id: str, raw_event: str, semantic_event: Dict[str, Any], 
                     cognitive_state: Dict[str, float], narrative: Dict[str, str]) -> ReplayFrame:
        timeline = self.get_or_create_timeline(execution_id)
        frame = ReplayFrame(
            execution_id=execution_id,
            timestamp=datetime.now(timezone.utc).timestamp(),
            raw_event=raw_event,
            semantic_event=semantic_event,
            cognitive_state=cognitive_state,
            narrative=narrative
        )
        timeline.add_frame(frame)
        return frame
    
    def get_timeline(self, execution_id: str) -> Optional[ExecutionTimeline]:
        return self.timelines.get(execution_id)
    
    def get_trajectory(self, execution_id: str) -> List[str]:
        timeline = self.timelines.get(execution_id)
        if timeline:
            return timeline.get_state_trajectory()
        return []
    
    def verify_narrative(self, execution_id: str) -> Dict[str, Any]:
        """Verify the consistency of narratives for an entire execution."""
        timeline = self.timelines.get(execution_id)
        if not timeline:
            return {"valid": False, "reason": "No timeline found", "consistency_score": 0.0}
        
        score = timeline.get_consistency_score()
        return {
            "execution_id": execution_id,
            "consistency_score": score,
            "valid": score >= 0.7,
            "reason": f"Consistency score: {score}. {'Narratives are generally consistent.' if score >= 0.7 else 'Narratives diverge from cognitive states.'}"
        }
    
    def stream_frames(self, execution_id: str) -> List[Dict[str, Any]]:
        """Return frames in order for frontend replay."""
        timeline = self.timelines.get(execution_id)
        if not timeline:
            return []
        
        frames = []
        for frame in timeline.frames:
            frames.append({
                "execution_id": frame.execution_id,
                "timestamp": frame.timestamp,
                "raw_event": frame.raw_event,
                "semantic_event": frame.semantic_event,
                "cognitive_state": frame.cognitive_state,
                "narrative": frame.narrative
            })
        return frames


# Global instance
replay_engine = ReplayEngine()
