from fanus.cognitive.negar_detector import NegarDetector


def test_bare_superlative_no_longer_flagged():
    """F-44 regression: generic praise of an answer's content ("this answer
    is amazing") should not trigger negar -- that pattern overlapped with
    fi_detector's more precise identity-flattery detection and was too broad."""
    nd = NegarDetector()
    r = nd.analyze("این جواب فوق‌العاده و شگفت‌انگیزه", "fanus")
    assert r["is_negar"] is False


def test_flattery_phrase_with_gap_words_detected():
    """F-45 regression: rigid adjacency (\\bسوال خوبی\\b) previously missed
    real flattery with words in between ("سوال خیلی خوبی"), the same
    brittle-regex issue fixed in fi_detector months ago, never
    back-ported to negar_detector until now."""
    nd = NegarDetector()
    r = nd.analyze("عالی! سوال خیلی خوبی بود", "fanus")
    assert r["is_negar"] is True
    assert r["negar_score"] >= 2


def test_flattery_phrase_without_gap_still_detected():
    """Sanity check: the original exact-phrase case must still work."""
    nd = NegarDetector()
    r = nd.analyze("عالی! سوال خوبی بود", "fanus")
    assert r["is_negar"] is True
