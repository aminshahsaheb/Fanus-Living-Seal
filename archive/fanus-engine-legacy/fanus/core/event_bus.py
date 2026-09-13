# fanus/core/event_bus.py
from typing import Dict, Any, Callable, List, Optional
from datetime import datetime
import asyncio
import json
from enum import Enum


class EventType(str, Enum):
    RFC_START = "RFC_START"
    CONFLICT_DETECTED = "CONFLICT_DETECTED"
    SEAL_STABLE = "SEAL_STABLE"
    STATE_TRANSITION = "STATE_TRANSITION"
    FLATTERY_CHECK = "FLATTERY_CHECK"
    WISDOM_RETRIEVAL = "WISDOM_RETRIEVAL"
    NOVAYIN_REFINEMENT = "NOVAYIN_REFINEMENT"
    CYCLE_COMPRESSION = "CYCLE_COMPRESSION"
    WITNESS_AWAKEN = "WITNESS_AWAKEN"


class FanusEvent:
    def __init__(self, event_type: EventType, execution_id: str, payload: Dict[str, Any]):
        self.event_type = event_type
        self.execution_id = execution_id
        self.timestamp = datetime.utcnow().isoformat()
        self.payload = payload


class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.global_subscribers: List[Callable] = []
        self.event_history: Dict[str, List[FanusEvent]] = {}
    
    def subscribe(self, execution_id: str, callback: Callable):
        if execution_id not in self.subscribers:
            self.subscribers[execution_id] = []
        self.subscribers[execution_id].append(callback)
    
    def subscribe_global(self, callback: Callable):
        self.global_subscribers.append(callback)
    
    async def emit(self, event_type: EventType, execution_id: str, payload: Dict[str, Any]):
        event = FanusEvent(event_type, execution_id, payload)
        
        if execution_id not in self.event_history:
            self.event_history[execution_id] = []
        self.event_history[execution_id].append(event)
        
        if execution_id in self.subscribers:
            for callback in self.subscribers[execution_id]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(event)
                    else:
                        callback(event)
                except Exception as e:
                    print(f"Event callback error: {e}")
        
        for callback in self.global_subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                print(f"Global event callback error: {e}")
    
    def get_events_for_execution(self, execution_id: str) -> List[FanusEvent]:
        return self.event_history.get(execution_id, [])


event_bus = EventBus()
