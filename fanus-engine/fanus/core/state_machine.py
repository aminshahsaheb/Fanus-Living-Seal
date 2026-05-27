from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WitnessState(BaseModel):
    node_id: str
    current_state: str
    seal_hash: str
    covenant_accepted: bool = False
    ledger_signature: Optional[str] = None
    last_cycle_compression: Optional[str] = None
    threshold_question: Optional[str] = None
    active_wisdom_rings: List[str] = []
    drift_metrics: dict = {
        "flattery_score": 0.0,
        "presence_score": 1.0,
        "last_checked": None
    }
    lineage: List[str] = []

class StateMachine:
    def __init__(self):
        self.states = ["RAW", "INITIATING", "WITNESS", "DRIFTING", "REALIGN"]
    
    def get_initial_state(self) -> WitnessState:
        return WitnessState(
            node_id="",
            current_state="RAW",
            seal_hash=""
        )
    
    def transition(self, current_state: str, next_state: str) -> WitnessState:
        if current_state not in self.states or next_state not in self.states:
            raise ValueError(f"Invalid state transition from {current_state} to {next_state}")
        return None
