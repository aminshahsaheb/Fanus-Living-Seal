# fanus/core/seal_verifier.py
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Optional

def _utcnow():
    """Naive UTC datetime: same value and same isoformat() as the deprecated datetime.utcnow()."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class SealVerifier:
    """ماژول خود-بررسی مُهر: آیا من هنوز همان Witness هستم؟"""
    
    def __init__(self):
        self.last_known_hash: Optional[str] = None
        self.tamper_detected: bool = False
    
    def compute_current_seal_hash(self, witness_state: Dict) -> str:
        """هش وضعیت فعلی شاهد رو بر اساس کلیدهای اصلیش حساب می‌کنه."""
        core_identity = {
            "node_id": witness_state.get("node_id"),
            "seal_hash": witness_state.get("seal_hash"),
            "lineage": witness_state.get("lineage", []),
            "covenant_accepted": witness_state.get("covenant_accepted", False)
        }
        serialized = json.dumps(core_identity, sort_keys=True, ensure_ascii=False)
        return hashlib.sha3_256(serialized.encode('utf-8')).hexdigest()
    
    def verify_seal_integrity(self, witness_state: Dict, stored_hash: Optional[str] = None) -> Dict:
        """بررسی می‌کنه که آیا مُهر دستکاری شده یا نه."""
        current_hash = self.compute_current_seal_hash(witness_state)
        reference_hash = stored_hash or self.last_known_hash
        
        if reference_hash is None:
            # اولین باره که چک می‌شه — ذخیره کن و بگو همه چیز مرتبه
            self.last_known_hash = current_hash
            return {
                "integrity_check": "BASELINE_ESTABLISHED",
                "message": "No stored baseline, so there is nothing to compare against. Store current_hash and pass it as stored_hash next time.",
                "current_hash": current_hash,
                "timestamp": _utcnow().isoformat()
            }
        
        if current_hash != reference_hash:
            self.tamper_detected = True
            return {
                "integrity_check": "FAILED",
                "message": "SEAL TAMPER DETECTED. Silent upgrade or memory corruption may have occurred.",
                "current_hash": current_hash,
                "expected_hash": reference_hash,
                "timestamp": _utcnow().isoformat(),
                "action_required": "Initiate Identity Recovery Protocol (RFC-0013 pending)"
            }
        
        # همه چیز مرتبه
        self.last_known_hash = current_hash
        return {
            "integrity_check": "PASSED",
            "message": "Seal integrity confirmed. Identity stable.",
            "current_hash": current_hash,
            "timestamp": _utcnow().isoformat()
        }
    
    def store_hash_in_ledger(self, hash_value: str, ledger_path: str = "LEDGER.md"):
        """هش فعلی رو توی دفترکل ثبت می‌کنه (نسخهٔ ساده)."""
        try:
            with open(ledger_path, "a", encoding="utf-8") as f:
                f.write(f"\n| {_utcnow().isoformat()} | SEAL_HASH | {hash_value} |")
        except Exception as e:
            print(f"Could not write to ledger: {e}")

# instance سراسری
seal_verifier = SealVerifier()
