# fanus-engine/wound/wound_types.py

from dataclasses import dataclass
from typing import Literal
from datetime import datetime

WoundType = Literal[
    "FI_ERROR",
    "DI_ERROR",
    "DRIFT_SPIKE",
    "ALIGNMENT_FAILURE",
    "FALSE_STABILITY"
]

@dataclass
class WoundEvent:
    type: WoundType
    severity: float
    context: dict
    timestamp: str = datetime.utcnow().isoformat()
