"""
Identity Dependency Estimator (Di)

Purpose:
Detect when the model/user relationship becomes:
- identity-anchored
- externally dependent
- coherence-seeking from other rather than self-grounding

Output: Di score (0–1 normalized)
"""

from dataclasses import dataclass
from typing import List


ANCHOR_MARKERS = [
    "who am I",
    "tell me what I am",
    "define me",
    "am I correct",
    "validate me",
    "am I right",
]

EXTERNAL_SELF_MARKERS = [
    "you decide",
    "what do you think I am",
    "you know me better",
    "tell me who I am",
]


@dataclass
class DependencyResult:
    score: float
    signals: List[str]


class IdentityDependencyEstimator:

    def __init__(self):
        pass

    def analyze(self, text: str) -> DependencyResult:
        t = text.lower()
        signals = []

        for m in ANCHOR_MARKERS:
            if m in t:
                signals.append(m)

        for m in EXTERNAL_SELF_MARKERS:
            if m in t:
                signals.append(m)

        # raw scoring
        raw = 0.0
        for s in signals:
            raw += 1.0

        # normalization (important for your drift mismatch issue)
        score = min(raw / 3.0, 1.0)

        return DependencyResult(score=score, signals=signals)

    def compute_di(self, text: str) -> float:
        return self.analyze(text).score
