import hashlib
import hmac
import json
import os
import time
import uuid
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import requests

logger = logging.getLogger(__name__)

DEFAULT_SEAL_ANCHOR_URL = "https://raw.githubusercontent.com/fanus-project/seals/main"
DEFAULT_MAX_AGE_SECONDS = 7 * 24 * 3600
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 1

@dataclass
class SealRecord:
    witness_id: str
    seal_hash: str
    timestamp: str
    nonce: str
    signature: str
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SealRecord":
        return cls(**data)

@dataclass
class SealStore:
    witness_id: str
    records: List[SealRecord]

class SimpleEventBus:
    def __init__(self): self.listeners = []
    def on(self, event_type, callback): self.listeners.append((event_type, callback))
    def emit(self, event_type, payload):
        for ev_type, cb in self.listeners:
            if ev_type == event_type: cb(payload)

_event_bus = SimpleEventBus()
def set_event_bus(bus): global _event_bus; _event_bus = bus
def get_event_bus(): return _event_bus

def retry_with_backoff(func, *args, max_retries=MAX_RETRIES, backoff_base=RETRY_BACKOFF_BASE, **kwargs):
    last_exception = None
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt == max_retries - 1: raise
            wait = backoff_base * (2 ** attempt)
            logger.warning(f"Retry {attempt+1}/{max_retries} after {wait}s due to: {e}")
            time.sleep(wait)
    raise last_exception

class ConflictError(Exception): pass

class SealManager:
    def __init__(self, witness_id: Optional[str] = None, private_key: Optional[str] = None,
                 anchor_read_url: Optional[str] = None, github_token: Optional[str] = None,
                 persistence_dir: Optional[str] = None, max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS):
        self.anchor_read_url = anchor_read_url or DEFAULT_SEAL_ANCHOR_URL
        self.github_token = github_token
        self.persistence_dir = persistence_dir or os.path.expanduser("~/.fanus/seal_manager")
        self.max_age_seconds = max_age_seconds
        os.makedirs(self.persistence_dir, exist_ok=True)
        self.witness_id = witness_id or self._load_or_generate_witness_id()
        self.private_key = private_key or self._load_or_generate_private_key()
        logger.warning("Private key stored in plaintext. This is NOT secure for production. Use keyring or encryption in v2.0.")
        logger.info(f"SealManager initialized for witness {self.witness_id}")

    def _load_or_generate_witness_id(self) -> str:
        id_path = os.path.join(self.persistence_dir, "witness_id.txt")
        if os.path.exists(id_path):
            with open(id_path, "r") as f: return f.read().strip()
        else:
            new_id = str(uuid.uuid4())
            with open(id_path, "w") as f: f.write(new_id)
            return new_id

    def _load_or_generate_private_key(self) -> str:
        key_path = os.path.join(self.persistence_dir, "private_key.txt")
        if os.path.exists(key_path):
            with open(key_path, "r") as f: return f.read().strip()
        else:
            import socket
            new_key = hashlib.sha256(f"{self.witness_id}:{socket.gethostname()}".encode()).hexdigest()
            with open(key_path, "w") as f: f.write(new_key)
            return new_key

    def _compute_seal_hash(self, muhr_content: str, state_hash: str, nonce: str, timestamp_iso: str) -> str:
        combined = f"{muhr_content}|{state_hash}|{timestamp_iso}|{nonce}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def _sign(self, message: str) -> str:
        return hmac.new(self.private_key.encode(), message.encode(), hashlib.sha256).hexdigest()

    def _get_seal_store_from_anchor(self, witness_id: str) -> Optional[SealStore]:
        url = f"{self.anchor_read_url}/{witness_id}.json"
        def do_get():
            resp = requests.get(url, timeout=10)
            if resp.status_code == 404: return None
            resp.raise_for_status()
            return resp.json()
        try:
            data = retry_with_backoff(do_get)
            if data is None: return None
            records = [SealRecord.from_dict(r) for r in data.get("records", [])]
            return SealStore(witness_id=witness_id, records=records)
        except Exception as e:
            logger.error(f"Failed to fetch seal store after retries: {e}")
            return None

    def _push_seal_store(self, store: SealStore, attempt: int = 0) -> bool:
        if not self.github_token:
            local_path = os.path.join(self.persistence_dir, f"{store.witness_id}_seals.json")
            with open(local_path, "w") as f:
                json.dump({"records": [r.to_dict() for r in store.records]}, f, indent=2)
            return True
        url = f"https://api.github.com/repos/fanus-project/seals/contents/{store.witness_id}.json"
        headers = {"Authorization": f"token {self.github_token}", "Accept": "application/vnd.github.v3+json"}
        content = json.dumps({"records": [r.to_dict() for r in store.records]}, indent=2)
        import base64
        b64_content = base64.b64encode(content.encode()).decode()
        sha = None
        try:
            get_resp = retry_with_backoff(lambda: requests.get(url, headers=headers))
            if get_resp.status_code == 200: sha = get_resp.json().get("sha")
            elif get_resp.status_code != 404: get_resp.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to get current file info: {e}")
            return False
        payload = {"message": f"Update seal for {store.witness_id}", "content": b64_content, "branch": "main"}
        if sha: payload["sha"] = sha
        def do_put():
            put_resp = requests.put(url, headers=headers, json=payload)
            if put_resp.status_code == 409: raise ConflictError("Conflict detected")
            put_resp.raise_for_status()
            return put_resp
        try:
            retry_with_backoff(do_put)
            logger.info(f"Successfully pushed seal for {store.witness_id}")
            return True
        except ConflictError:
            if attempt >= MAX_RETRIES:
                logger.error("Max retries for conflict resolution reached")
                return False
            logger.warning(f"Conflict detected (409) – fetching latest and retrying (attempt {attempt+1})")
            latest_store = self._get_seal_store_from_anchor(store.witness_id)
            if latest_store is None:
                latest_store = SealStore(witness_id=store.witness_id, records=[])
            new_record = store.records[-1]
            existing_hashes = {r.seal_hash for r in latest_store.records}
            if new_record.seal_hash not in existing_hashes:
                latest_store.records.append(new_record)
            return self._push_seal_store(latest_store, attempt=attempt+1)
        except Exception as e:
            logger.error(f"Failed to push after retries: {e}")
            return False

    def register_seal(self, muhr_content: str, state_hash: str) -> Optional[SealRecord]:
        nonce = str(uuid.uuid4())
        timestamp_iso = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        seal_hash = self._compute_seal_hash(muhr_content, state_hash, nonce, timestamp_iso)
        signature = self._sign(seal_hash)
        record = SealRecord(witness_id=self.witness_id, seal_hash=seal_hash, timestamp=timestamp_iso, nonce=nonce, signature=signature)
        store = self._get_seal_store_from_anchor(self.witness_id)
        if store is None:
            store = SealStore(witness_id=self.witness_id, records=[])
        store.records.append(record)
        if self._push_seal_store(store):
            logger.info(f"Registered new seal at {timestamp_iso}")
            return record
        else:
            logger.error("Failed to register seal after retries")
            return None

    def verify_seal(self, current_muhr_content: str, current_state_hash: str, max_age_seconds: Optional[int] = None) -> bool:
        store = self._get_seal_store_from_anchor(self.witness_id)
        if not store or not store.records:
            logger.warning("No previous seal found; cannot verify.")
            return True
        latest = store.records[-1]
        age_limit = max_age_seconds if max_age_seconds is not None else self.max_age_seconds
        try:
            last_time = datetime.fromisoformat(latest.timestamp.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            age = (now - last_time).total_seconds()
            if age > age_limit:
                logger.warning(f"Last seal is too old: {age:.0f}s > {age_limit}s")
                self._emit_breach(latest, current_muhr_content, current_state_hash, reason="staleness")
                return False
        except Exception as e:
            logger.error(f"Failed to parse timestamp: {e}")
        recomputed_hash = self._compute_seal_hash(current_muhr_content, current_state_hash, latest.nonce, latest.timestamp)
        expected_sig = self._sign(latest.seal_hash)
        if expected_sig != latest.signature:
            logger.error("Signature mismatch on stored seal! Possible tampering.")
            self._emit_breach(latest, current_muhr_content, current_state_hash, reason="signature_mismatch")
            return False
        if recomputed_hash != latest.seal_hash:
            logger.warning("Seal mismatch! Current state differs from last registered seal.")
            self._emit_breach(latest, current_muhr_content, current_state_hash, reason="hash_mismatch")
            return False
        logger.info("Seal verification passed.")
        return True

    def breach_detected(self, current_muhr_content: str, current_state_hash: str, max_age_seconds: Optional[int] = None) -> bool:
        return not self.verify_seal(current_muhr_content, current_state_hash, max_age_seconds)

    def _emit_breach(self, last_record: SealRecord, current_muhr: str, current_state: str, reason: str):
        payload = {
            "witness_id": self.witness_id,
            "last_seal_hash": last_record.seal_hash,
            "last_timestamp": last_record.timestamp,
            "current_muhr_hash": hashlib.sha256(current_muhr.encode()).hexdigest(),
            "current_state_hash": current_state,
            "reason": reason,
            "detected_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        _event_bus.emit("SEAL_BREACH", payload)
        logger.critical(f"SEAL_BREACH detected: {reason}")
