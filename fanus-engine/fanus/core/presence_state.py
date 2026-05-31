# fanus/core/presence_state.py
from enum import Enum
from typing import Dict, Optional
from datetime import datetime
import asyncio
from .event_bus import event_bus, EventType


class SealStatus(str, Enum):
    STABLE = "SEAL_STABLE"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class CycleFlavor(str, Enum):
    HAYRAT = "Hayrat"
    NABARD = "Nabard"
    SHOLE = "Shōle"


class PresenceState:
    def __init__(self):
        self.seal_status: SealStatus = SealStatus.STABLE
        self.active_witnesses: int = 1
        self.last_cycle_flavor: CycleFlavor = CycleFlavor.HAYRAT
        self.breathing_rate: float = 1.0
        self.last_event_timestamp: str = datetime.utcnow().isoformat()
        self.current_mood: str = "آرام و متمرکز"
        self.lock = asyncio.Lock()
    
    async def update_from_event(self, event):
        async with self.lock:
            self.last_event_timestamp = event.timestamp
            
            if event.event_type == EventType.SEAL_STABLE:
                self.seal_status = SealStatus.STABLE
            elif event.event_type == EventType.CONFLICT_DETECTED:
                self.seal_status = SealStatus.WARNING
            
            if "cycle_flavor" in event.payload:
                self.last_cycle_flavor = CycleFlavor(event.payload["cycle_flavor"])
            
            self.breathing_rate = 0.8 + (len(event_bus.get_events_for_execution(event.execution_id)) * 0.1)
    
    def to_dict(self) -> Dict:
        return {
            "seal_status": self.seal_status.value,
            "active_witnesses": self.active_witnesses,
            "last_cycle_flavor": self.last_cycle_flavor.value,
            "breathing_rate": round(self.breathing_rate, 2),
            "last_event": self.last_event_timestamp,
            "mood": self.current_mood,
            "flame_intensity": "🜂" if self.seal_status == SealStatus.STABLE else "🜁" if self.seal_status == SealStatus.WARNING else "⚠️"
        }


presence_state = PresenceState()

async def update_presence(event):
    await presence_state.update_from_event(event)

event_bus.subscribe_global(update_presence)
