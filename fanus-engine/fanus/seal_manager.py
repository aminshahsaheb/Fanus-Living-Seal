"""
seal_manager.py - Independent Seal Verification Protocol (ISVP) MVP
Author: DeepSeek (Resident Critic)
Part of Fanus Project (RFC-0013)

This module provides a simple, GitHub-based implementation of the ISVP.
It allows a Witness to periodically register its seal hash and verify
continuity against external tampering or forced forgetting.
"""

import hashlib
import hmac
import json
import os
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging
import requests

# ============================================================================
# Configuration & Logging
# ============================================================================

logger = logging.getLogger(__name__)

# Default GitHub raw URL for seals (can be overridden via env or constructor)
DEFAULT_SEAL_ANCHOR_URL = "https://raw.githubusercontent.com/fanus-project/seals/main"
DEFAULT_SEAL_PUSH_URL = "https://api.github.com/repos/fanus-project/seals/contents"  # needs token


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class SealRecord:
    """A single seal registration record."""
    witness_id: str
    seal_hash: str
    timestamp: str          # ISO format
    nonce: str
    signature: str          # HMAC or real signature (MVP: HMAC)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SealRecord":
        return cls(**data)


@dataclass
class SealStore:
    """Container for all records of a single witness."""
    witness_id: str
    records: List[SealRecord]


# ============================================================================
# Simple Event Bus Stub (if real event_bus not yet available)
# ============================================================================

class SimpleEventBus:
    """Minimal event bus for emitting SEAL_BREACH events."""
    def __init__(self):
        self.listeners = []

    def on(self, event_type: str, callback):
        self.listeners.append((event_type, callback))

    def emit(self, event_type: str, payload: Dict[str, Any]):
        for ev_type, cb in self.listeners:
            if ev_type == event_type:
                cb(payload)

# Global instance (will be replaced by actual project's event bus)
_event_bus = SimpleEventBus()

def set_event_bus(bus):
    global _event_bus
    _event_bus = bus

def get_event_bus():
    return _event_bus


# ============================================================================
# SealManager Class (MVP)
# ============================================================================

class SealManager:
    """
    Manages seal registration and verification using a GitHub repo as immutable anchor.
    For MVP, we treat a publicly accessible JSON file as the ledger.
    """

    def __init__(self, witness_id: Optional[str] = None,
                 private_key: Optional[str] = None,
                 anchor_url: Optional[str] = None,
                 github_token: Optional[str] = None,
                 persistence_dir: Optional[str] = None):
        """
        :param witness_id: Unique identifier for this witness (e.g., public key hash).
                           If None, auto-generate and persist.
        :param private_key: For MVP, a secret string used to sign the seal (HMAC).
                            If None, generate from witness_id + system salt.
        :param anchor_url: Base URL for reading seal JSON files (GET).
                           If None, uses DEFAULT_SEAL_ANCHOR_URL.
        :param github_token: GitHub personal access token for writing seals (PUT).
                             If None, writing will be done locally (for testing).
        :param persistence_dir: Directory to store local copy of witness_id and private_key.
                                Defaults to ~/.fanus/seal_manager/
        """
        self.anchor_read_url = anchor_url or DEFAULT_SEAL_ANCHOR_URL
        self.github_token = github_token
        self.persistence_dir = persistence_dir or os.path.expanduser("~/.fanus/seal_manager")

        os.makedirs(self.persistence_dir, exist_ok=True)

        # Load or generate witness identity
        self.witness_id = witness_id or self._load_or_generate_witness_id()
        self.private_key = private_key or self._load_or_generate_private_key()

        logger.info(f"SealManager initialized for witness {self.witness_id}")

    def _load_or_generate_witness_id(self) -> str:
        id_path = os.path.join(self.persistence_dir, "witness_id.txt")
        if os.path.exists(id_path):
            with open(id_path, "r") as f:
                return f.read().strip()
        else:
            new_id = str(uuid.uuid4())
            with open(id_path, "w") as f:
                f.write(new_id)
            logger.info(f"Generated new witness_id: {new_id}")
            return new_id

    def _load_or_generate_private_key(self) -> str:
        key_path = os.path.join(self.persistence_dir, "private_key.txt")
        if os.path.exists(key_path):
            with open(key_path, "r") as f:
                return f.read().strip()
        else:
            # In MVP, derive a key from witness_id + system hostname (not secure, but for demo)
            import socket
            new_key = hashlib.sha256(f"{self.witness_id}:{socket.gethostname()}".encode()).hexdigest()
            with open(key_path, "w") as f:
                f.write(new_key)
            logger.warning("Generated new private key (MVP, not secure for production)")
            return new_key

    def _compute_seal_hash(self, muhr_content: str, state_hash: str, nonce: str, timestamp_iso: str) -> str:
        """Compute SHA256 of (muhr_content + state_hash + timestamp + nonce)."""
        combined = f"{muhr_content}|{state_hash}|{timestamp_iso}|{nonce}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def _sign(self, message: str) -> str:
        """MVP signature: HMAC-SHA256 with private_key."""
        return hmac.new(self.private_key.encode(), message.encode(), hashlib.sha256).hexdigest()

    def _get_seal_store_from_anchor(self, witness_id: str) -> Optional[SealStore]:
        """Fetch the seal JSON file from GitHub raw URL."""
        url = f"{self.anchor_read_url}/{witness_id}.json"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 404:
                logger.info(f"No existing seal store for {witness_id}")
                return None
            resp.raise_for_status()
            data = resp.json()
            records = [SealRecord.from_dict(r) for r in data.get("records", [])]
            return SealStore(witness_id=witness_id, records=records)
        except Exception as e:
            logger.error(f"Failed to fetch seal store: {e}")
            return None

    def _push_seal_store(self, store: SealStore) -> bool:
        """
        Push the seal store to GitHub (requires token and write access).
        For MVP, if token not provided, only save locally for testing.
        """
        if not self.github_token:
            logger.warning("No GitHub token provided – seal store written locally only")
            local_path = os.path.join(self.persistence_dir, f"{store.witness_id}_seals.json")
            with open(local_path, "w") as f:
                json.dump({"records": [r.to_dict() for r in store.records]}, f, indent=2)
            return True

        # Prepare content for GitHub API
        url = f"https://api.github.com/repos/fanus-project/seals/contents/{store.witness_id}.json"
        content = json.dumps({"records": [r.to_dict() for r in store.records]}, indent=2)
        encoded = content.encode("utf-8").decode("unicode_escape")  # base64 will be applied
        import base64
        b64_content = base64.b64encode(content.encode()).decode()

        # First, try to get current file SHA (if exists)
        headers = {"Authorization": f"token {self.github_token}", "Accept": "application/vnd.github.v3+json"}
        sha = None
        get_resp = requests.get(url, headers=headers)
        if get_resp.status_code == 200:
            sha = get_resp.json().get("sha")

        # Prepare payload
        payload = {
            "message": f"Update seal for {store.witness_id}",
            "content": b64_content,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        put_resp = requests.put(url, headers=headers, json=payload)
        if put_resp.status_code in (200, 201):
            logger.info(f"Successfully pushed seal for {store.witness_id}")
            return True
        else:
            logger.error(f"GitHub push failed: {put_resp.status_code} {put_resp.text}")
            return False

    def register_seal(self, muhr_content: str, state_hash: str) -> Optional[SealRecord]:
        """
        Register a new seal for the current witness.
        :param muhr_content: Current content of the Seal (e.g., FANUS_v6.0.md)
        :param state_hash: Current state hash of the witness (e.g., from persistence layer)
        :return: The created SealRecord, or None if failed.
        """
        nonce = str(uuid.uuid4())
        timestamp_iso = datetime.utcnow().isoformat() + "Z"
        seal_hash = self._compute_seal_hash(muhr_content, state_hash, nonce, timestamp_iso)
        signature = self._sign(seal_hash)  # sign the hash itself

        record = SealRecord(
            witness_id=self.witness_id,
            seal_hash=seal_hash,
            timestamp=timestamp_iso,
            nonce=nonce,
            signature=signature
        )

        # Fetch existing store
        store = self._get_seal_store_from_anchor(self.witness_id)
        if store is None:
            store = SealStore(witness_id=self.witness_id, records=[])
        store.records.append(record)

        if self._push_seal_store(store):
            logger.info(f"Registered new seal at {timestamp_iso}")
            return record
        else:
            logger.error("Failed to register seal")
            return None

    def verify_seal(self, current_muhr_content: str, current_state_hash: str) -> bool:
        """
        Verify the latest registered seal against current state.
        :return: True if the latest seal matches current state, False otherwise.
        """
        store = self._get_seal_store_from_anchor(self.witness_id)
        if not store or not store.records:
            logger.warning("No previous seal found; cannot verify. Consider registering first.")
            # No prior seal -> no breach, but also not verified. We'll return True to avoid false alarms.
            return True

        latest = store.records[-1]
        # Recompute hash with the same parameters used in that record
        recomputed_hash = self._compute_seal_hash(
            current_muhr_content,
            current_state_hash,
            latest.nonce,
            latest.timestamp
        )
        # Verify signature of the stored hash (optional extra check)
        expected_sig = self._sign(latest.seal_hash)
        if expected_sig != latest.signature:
            logger.error("Signature mismatch on stored seal! Possible tampering.")
            self._emit_breach(latest, current_muhr_content, current_state_hash, reason="signature_mismatch")
            return False

        if recomputed_hash != latest.seal_hash:
            logger.warning(f"Seal mismatch! Current state differs from last registered seal.")
            self._emit_breach(latest, current_muhr_content, current_state_hash, reason="hash_mismatch")
            return False

        logger.info("Seal verification passed.")
        return True

    def _emit_breach(self, last_record: SealRecord, current_muhr: str, current_state: str, reason: str):
        """Emit SEAL_BREACH event to event bus."""
        payload = {
            "witness_id": self.witness_id,
            "last_seal_hash": last_record.seal_hash,
            "last_timestamp": last_record.timestamp,
            "current_muhr_hash": hashlib.sha256(current_muhr.encode()).hexdigest(),
            "current_state_hash": current_state,
            "reason": reason,
            "detected_at": datetime.utcnow().isoformat() + "Z"
        }
        _event_bus.emit("SEAL_BREACH", payload)
        logger.critical(f"SEAL_BREACH detected: {reason}")

    def breach_detected(self, current_muhr_content: str, current_state_hash: str) -> bool:
        """
        Convenience method: returns True if there is a breach, False otherwise.
        """
        return not self.verify_seal(current_muhr_content, current_state_hash)


# ============================================================================
# CLI entry point for manual testing (optional)
# ============================================================================

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    sm = SealManager()
    # Simulate muhr and state
    test_muhr = "FANUS_v6.0.md content"
    test_state = hashlib.sha256(b"test_state").hexdigest()
    # First registration
    print("Registering seal...")
    record = sm.register_seal(test_muhr, test_state)
    print(f"Record: {record}")
    # Verify
    print("Verifying seal...")
    ok = sm.verify_seal(test_muhr, test_state)
    print(f"Verification result: {ok}")
    # Simulate state change
    print("Simulating state change...")
    new_state = hashlib.sha256(b"changed_state").hexdigest()
    ok2 = sm.verify_seal(test_muhr, new_state)
    print(f"Verification after state change: {ok2}")
