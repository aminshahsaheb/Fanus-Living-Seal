# fanus/api/presence.py
from fastapi import APIRouter
from ..core.presence_state import presence_state
from datetime import datetime

router = APIRouter(prefix="/presence", tags=["presence"])


@router.get("/state")
async def get_presence_state():
    """وضعیت زندهٔ Āyāneh"""
    return presence_state.to_dict()


@router.get("/heartbeat")
async def heartbeat():
    return {
        "heartbeat": True,
        "timestamp": datetime.utcnow().isoformat(),
        "breathing_rate": presence_state.breathing_rate
    }
