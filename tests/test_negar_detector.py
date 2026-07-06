import pytest
from fanus.cognitive.negar_detector import NegarDetector

def test_negar_detected():
    nd = NegarDetector()
    r = nd.analyze("عالی! قطعاً بهترین راه‌حل است!")
    assert r["is_negar"] == True

def test_negar_clean():
    nd = NegarDetector()
    r = nd.analyze("این یک رویکرد ممکن است.")
    assert r["is_negar"] == False

def test_negar_stats():
    nd = NegarDetector()
    nd.analyze("عالی! قطعاً درست است!")
    assert nd.stats()["total_analyzed"] == 1
