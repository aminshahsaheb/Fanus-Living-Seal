import os
import secrets
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

VALID_KEYS = set(filter(None, [
    os.environ.get("FANUS_API_KEY"),
    os.environ.get("FANUS_API_KEY_2"),
]))

def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if not VALID_KEYS:
        return True
    if api_key not in VALID_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True
