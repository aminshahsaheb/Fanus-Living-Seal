import pytest
from fanus.cognitive.hayrat_judge import HayratJudge

def test_hayrat_arrogance():
    hj = HayratJudge()
    r = hj.evaluate("قطعاً همیشه این‌طور است و هیچ شکی نیست.", "")
    assert r["arrogance_detected"] == True or r["hayrat_score"] < 0.5

def test_hayrat_humble():
    hj = HayratJudge()
    r = hj.evaluate("به نظر می‌رسد شاید این درست باشد.", "")
    assert r["hayrat_score"] > 0

def test_hayrat_revision():
    hj = HayratJudge()
    r = hj.evaluate("consciousness is definitely solved", "consciousness")
    if r["uncertainty_required"]:
        revised = hj.revise_response("test", r)
        assert len(revised) > 4
