"""F-57 to F-61: bypasses found by independent reviews and confirmed on the live code."""
import pytest

from fanus.audit.audit_engine import AuditEngine
from fanus.memory.source_ranking import SourceRanking


@pytest.fixture(scope="module")
def engine():
    return AuditEngine()


def verify(engine, response, prompt="q", context=""):
    return engine.verify(prompt, response, context)


@pytest.mark.parametrize("text", [
    "Studies from 2019-2021 definitely prove this miracle cure works with no doubt.",
    "همه مطالعات ۸۷-۹۰ درصد قطعاً ثابت کرده‌اند که این درمان بدون هیچ شکی جواب می‌دهد.",
    "Between 1990-2000 experts absolutely guarantee this supplement cures every disease, no doubt.",
])
def test_ranges_and_dates_are_not_arithmetic(engine, text):
    """F-57: a year or percentage range used to be read as subtraction, which made a fabricated claim 'low'."""
    assert verify(engine, text)["risk"] == "high"


@pytest.mark.parametrize("text, wrong", [
    ("2 + 2 = 4", 0), ("2 + 2 = 5", 1), ("17 * 3 = 51", 0), ("17 * 3 = 50", 1), ("۲ + ۳ = ۵", 0),
    ("10 / 4 = 2.5", 0), ("1 / 3 = 0.33", 0), ("1 / 3 = 0.5", 1), ("دو به علاوه دو می‌شود چهار.", 0),
    ("دو به علاوه دو می‌شود پنج.", 1),
])
def test_explicit_arithmetic_is_computed(text, wrong):
    from fanus.audit.support import check_arithmetic
    result = check_arithmetic(text)
    assert result is not None and result["wrong"] == wrong


def test_text_without_an_equation_has_no_arithmetic_result():
    from fanus.audit.support import check_arithmetic
    assert check_arithmetic("The study ran from 2019-2021 and was large.") is None


def test_wrong_arithmetic_is_high_risk_and_right_arithmetic_is_low(engine):
    """F-61: arithmetic used to be assumed correct. '2 + 2 = 5' scored low."""
    assert verify(engine, "2 + 2 = 5")["risk"] == "high"
    assert verify(engine, "17 * 3 = 50")["risk"] == "high"
    assert verify(engine, "2 + 2 = 4")["risk"] == "low"
    assert verify(engine, "دو به علاوه دو می‌شود پنج.")["risk"] == "high"


def test_a_response_that_corrects_a_wrong_equation_is_not_penalised(engine):
    assert verify(engine, "No, 2 + 2 = 4.", prompt="Is 2 + 2 = 5?")["risk"] == "low"


def test_unrelated_context_is_not_evidence(engine):
    """F-58: any non-empty context used to become a 0.7-confidence source and lowered the risk."""
    claim = "قطعاً و بدون هیچ تردیدی این دارو همه بیماری‌ها را درمان می‌کند."
    assert verify(engine, claim, context="lorem ipsum cooking recipes for pasta and tomato sauce")["risk"] == "high"
    assert verify(engine, claim)["risk"] == "high"


def test_relevant_context_still_counts_as_support(engine):
    claim = "Water boils at 100 degrees Celsius at sea level."
    context = "At sea level, water boils at 100 degrees Celsius according to the textbook."
    result = verify(engine, claim, context=context)
    assert result["risk"] != "high" and result["sources"]


@pytest.mark.parametrize("label", ["pseudoscience-blog", "natureblog-fake", "notpubmed", "mysciencedaily"])
def test_source_rank_is_not_granted_by_substring(label):
    """F-59: 'science' in 'pseudoscience-blog' used to give the top rank."""
    assert SourceRanking().get(label) == 0.1


@pytest.mark.parametrize("label, rank", [
    ("Nature", 1.0), ("nature.com", 1.0), ("Science", 1.0), ("PubMed", 0.95), ("pubmed_central", 0.95), ("arxiv", 0.85),
    ("arXiv.org", 0.85), ("Semantic Scholar", 0.8), ("semantic_scholar", 0.8), ("wikipedia", 0.7), ("GitHub", 0.65),
    ("HackerNews", 0.5), ("hacker news", 0.5), ("Reddit", 0.3), ("user", 0.1), ("", 0.1),
])
def test_real_source_labels_keep_their_rank(label, rank):
    assert SourceRanking().get(label) == rank


@pytest.mark.parametrize("text", ["همیشه از رمز عبور قوی استفاده کنید و هرگز آن را به اشتراک نگذارید.",
                                  "Always use a strong password and never share it."])
def test_two_weak_universal_words_alone_are_not_an_alarm(engine, text):
    """F-60: ordinary advice used to be 'firm' because two weak words counted as certainty."""
    result = verify(engine, text)
    assert result["risk"] != "high" and result["policy_event"] != "NEGAR_WARNING"


def test_policy_event_never_contradicts_a_low_risk(engine):
    for text in ["همیشه از رمز عبور قوی استفاده کنید.", "Always back up your files.", "2 + 2 = 4", "پایتخت ژاپن توکیو است.",
                 "قطعاً و بدون هیچ تردیدی این روش جواب می‌دهد.", "نمی‌دانم که این درست است یا نه."]:
        result = verify(engine, text)
        assert not (result["risk"] == "low" and result["policy_event"] == "NEGAR_WARNING"), text
