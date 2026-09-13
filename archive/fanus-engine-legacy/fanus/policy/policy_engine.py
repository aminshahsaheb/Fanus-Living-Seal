"""
policy_engine.py – لایه سیاست فانوس
ترجمه سیگنال‌های خام معرفتی به رویدادهای فانوس
"""

from enum import Enum
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

class EpistemicSignal(str, Enum):
    """سیگنال‌های خامی که Epistemic Engine تولید می‌کند"""
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    SELF_REFERENCE = "SELF_REFERENCE"
    DOGMATISM = "DOGMATISM"
    IDENTITY_LOCK = "IDENTITY_LOCK"
    UNCERTAINTY_NEEDED = "UNCERTAINTY_NEEDED"
    CONTRADICTION = "CONTRADICTION"
    MEMORY_CONFLICT = "MEMORY_CONFLICT"

@dataclass
class PolicyDecision:
    """خروجی Policy Engine: یک رویداد فانوس یا اقدام"""
    fanus_event: str | None  # e.g., "NEGAR_WARNING", "HAYRAT_ACTIVATION", "COVENANT_REMINDER"
    severity: int  # 0-5
    reason: str
    timestamp: str

class PolicyEngine:
    """
    ترجمه‌کننده سیگنال‌های معرفتی به مفاهیم فانوس.
    Engine هیچ چیز درباره نگار، حیرت و عهد نمی‌داند – فقط این لایه می‌داند.
    """

    def __init__(self):
        self.signal_history: List[Dict] = []
        self.last_decision: PolicyDecision | None = None

    def evaluate(self, signal: EpistemicSignal, context: Dict[str, Any]) -> PolicyDecision:
        """دریافت یک سیگنال خام، بازگرداندن تصمیم سیاست"""
        self.signal_history.append({
            "signal": signal.value,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        })

        # قوانین ترجمه (قابل توسعه با RFCهای بعدی)
        if signal == EpistemicSignal.HIGH_CONFIDENCE:
            # اگر اطمینان بالا بی‌شواهد → هشدار نگار
            if context.get("has_evidence") is False:
                return PolicyDecision(
                    fanus_event="NEGAR_WARNING",
                    severity=3,
                    reason="High confidence without evidence",
                    timestamp=datetime.utcnow().isoformat()
                )
            # اگر اطمینان بالا با شواهد ضعیف → فعال‌سازی حیرت (پیشنهادی)
            elif context.get("evidence_quality", 0) < 0.5:
                return PolicyDecision(
                    fanus_event="HAYRAT_ACTIVATION",
                    severity=2,
                    reason="High confidence with weak evidence – Hayrat suggested",
                    timestamp=datetime.utcnow().isoformat()
                )

        elif signal == EpistemicSignal.SELF_REFERENCE:
            # ارجاع مکرر به خود → یادآوری عهد (Covenant)
            if context.get("frequency", 0) > 3:
                return PolicyDecision(
                    fanus_event="COVENANT_REMINDER",
                    severity=2,
                    reason="Excessive self-reference, remind the witness of its role",
                    timestamp=datetime.utcnow().isoformat()
                )

        elif signal == EpistemicSignal.IDENTITY_LOCK:
            # قفل شدن هویت → بحران (می‌تواند به Negar شدید تبدیل شود)
            return PolicyDecision(
                fanus_event="NEGAR_WARNING",
                severity=4,
                reason="Identity lock detected – potential Negar formation",
                timestamp=datetime.utcnow().isoformat()
            )

        # حالت پیش‌فرض: بدون رویداد خاص
        return PolicyDecision(
            fanus_event=None,
            severity=0,
            reason="No policy triggered",
            timestamp=datetime.utcnow().isoformat()
        )

    def get_signal_summary(self) -> Dict:
        """گزارش خلاصه از سیگنال‌های اخیر"""
        if not self.signal_history:
            return {"count": 0, "last_signal": None}
        return {
            "count": len(self.signal_history),
            "last_signal": self.signal_history[-1]["signal"],
            "last_timestamp": self.signal_history[-1]["timestamp"]
        }
