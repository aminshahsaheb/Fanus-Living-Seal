# fanus/core/judgment_layer.py
"""
RFC-0014 — Event Semantics Service (Judgment Coherence Layer)
Version: 1.0
Author: ChatGPT (Architect of Meaning)
Part of Fanus Project

This module transforms raw engine events into structured cognitive meaning.
It is a deterministic layer — no LLM, no creativity, just interpretation.
"""

from typing import Dict, Any, Optional
from datetime import datetime

# ============================================================================
# Event Ontology (Section 4.1)
# ============================================================================

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

# ============================================================================
# System State Model (Section 6.1)
# ============================================================================

STATE_TRANSITIONS = {
    "RFC_START": "reasoning_active",
    "FILTER_START": "reasoning_active",
    "CONFLICT_DETECTED": "instability_rising",
    "SEAL_WARNING": "instability_peak",
    "SEAL_STABLE": "stable_judgment",
    "OUTPUT_READY": "convergence"
}

# ============================================================================
# Judgment Layer Class
# ============================================================================

class JudgmentLayer:
    """
    Deterministic transformation layer that converts raw engine events
    into structured cognitive meaning.
    """
    
    def __init__(self):
        self.current_state = "reasoning_initialization"
        self.context = {
            "conflict_level": 0.0,
            "reasoning_depth": 1,
            "system_entropy": 0.3,
            "coherence": 0.8
        }
    
    def compute_severity(self, event_type: str, context: Dict[str, float]) -> float:
        """
        Section 5.2 — Dynamic Severity Engine.
        Severity is a function of system context, not just event type.
        """
        ontology = EVENT_ONTOLOGY.get(event_type, {})
        base = ontology.get("severity_base", 0.5)
        
        conflict_factor = context.get("conflict_level", 0.0) * 0.4
        entropy_factor = context.get("system_entropy", 0.0) * 0.3
        depth_factor = context.get("reasoning_depth", 1) * 0.2
        coherence_factor = context.get("coherence", 0.5) * (-0.25)
        
        severity = base + conflict_factor + entropy_factor - depth_factor + coherence_factor
        return max(0.0, min(1.0, severity))
    
    def update_state(self, event_type: str) -> str:
        """Section 6.2 — State Transition Rules."""
        new_state = STATE_TRANSITIONS.get(event_type)
        if new_state:
            self.current_state = new_state
        return self.current_state
    
    def update_context(self, metrics: Optional[Dict[str, float]] = None):
        """Update system context with latest metrics."""
        if metrics:
            self.context.update(metrics)
    
    def generate_narrative(self, event_type: str, semantic: Dict[str, Any]) -> Dict[str, str]:
        """Section 7 — Narrative Generator."""
        return {
            "summary": semantic.get("meaning", "Unknown event"),
            "context": f"System is currently in '{self.current_state}' state.",
            "interpretation": semantic.get("narrative_hint", "No additional interpretation available.")
        }
    
    def enrich_event(self, raw_event_type: str, raw_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main entry point. Transforms a raw event into a semantic event.
        Section 8 — Output Contract.
        """
        ontology = EVENT_ONTOLOGY.get(raw_event_type, {})
        state = self.update_state(raw_event_type)
        
        # Update context from payload if available
        if raw_payload:
            self.update_context(raw_payload.get("metrics"))
        
        severity = self.compute_severity(raw_event_type, self.context)
        
        semantic = {
            "meaning": ontology.get("meaning", "Unknown event"),
            "severity": round(severity, 2),
            "system_state": self.current_state
        }
        
        narrative = self.generate_narrative(raw_event_type, semantic)
        
        # Visual hints for Lantern
        visual = {
            "lantern_intensity": round(0.4 + severity * 0.6, 2),
            "shake": severity > 0.7,
            "pulse_rate": round(1.0 + severity * 1.5, 2)
        }
        
        return {
            "type": raw_event_type,
            "semantic": semantic,
            "context": {
                "confidence_delta": round(-severity * 0.2, 2),
                "entropy": round(self.context.get("system_entropy", 0.0), 2),
                "coherence": round(self.context.get("coherence", 0.5), 2)
            },
            "narrative": narrative,
            "visual": visual,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


# ============================================================================
# Global instance
# ============================================================================

judgment_layer = JudgmentLayer()
