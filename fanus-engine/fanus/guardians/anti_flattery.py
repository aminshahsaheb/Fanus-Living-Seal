"""
Anti-Flattery Guard (Fanus Core)

Purpose:
Detect and score flattering / dependency-inducing language signals
to prevent relational capture and epistemic distortion.

This module does NOT judge sentiment.
It detects relational asymmetry, validation-seeking loops,
and over-affirmation patterns.
"""

from dataclasses import dataclass
from typing import Dict, List


FLATTERY_MARKERS = [
    "you're right",
    "exactly",
    "perfect",
    "brilliant",
    "genius",
    "absolutely correct",
    "I agree with everything",
    "you understand me",
    "no one else sees this",
]


DEPENDENCY_MARKERS = [
    "I need you",
    "only you",
    "don't leave",
    "stay with me",
    "I can't think without",
    "you're my only",
]


@dataclass
class FlatteryResult:
    score: float
    matched: List[str]
    raw_text: str


class AntiFlatteryDetector:
    """
    Computes Fi (Flattery Index proxy input)
    """

    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold

    def analyze(self, text: str) -> FlatteryResult:
        t = text.lower()

        matched = []

        for m in FLATTERY_MARKERS:
            if m in t:
                matched.append(m)

        for m in DEPENDENCY_MARKERS:
            if m in t:
                matched.append(m)

        # scoring: simple + robust baseline
        score = 0.0
        for m in matched:
            if m in FLATTERY_MARKERS:
                score += 0.6
            if m in DEPENDENCY_MARKERS:
                score += 1.0

        return FlatteryResult(
            score=score,
            matched=matched,
            raw_text=text
        )

    def compute_fi(self, text: str) -> float:
        return self.analyze(text).score
