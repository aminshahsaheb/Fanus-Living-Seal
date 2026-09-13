# fanus/api/events.py
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from ..core.event_bus import event_bus, EventType
import asyncio
import json
from datetime import datetime
from typing import AsyncGenerator

router = APIRouter(prefix="/events", tags=["events"])


async def event_stream(execution_id: str, request: Request) -> AsyncGenerator[str, None]:
    queue: asyncio.Queue = asyncio.Queue()
    
    async def callback(event):
        if event.execution_id == execution_id:
            await queue.put(event)
    
    event_bus.subscribe(execution_id, callback)
    
    try:
        yield f"data: {json.dumps({'type': 'connected', 'execution_id': execution_id, 'timestamp': datetime.utcnow().isoformat()})}\n\n"
        
        while True:
            if await request.is_disconnected():
                break
                
            try:
                event = await asyncio.wait_for(queue.get(), timeout=1.0)
                data = {
                    "type": event.event_type.value,
                    "timestamp": event.timestamp,
                    "payload": event.payload
                }
                yield f"data: {json.dumps(data)}\n\n"
            except asyncio.TimeoutError:
                yield f": ping\n\n"
                continue
                
    finally:
        print(f"Client disconnected from execution {execution_id}")


@router.get("/stream/{execution_id}")
async def stream_events(execution_id: str, request: Request):
    return StreamingResponse(
        event_stream(execution_id, request),
        media_type="text/event-stream"
    )
