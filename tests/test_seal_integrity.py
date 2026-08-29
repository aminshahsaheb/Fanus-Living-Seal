from fanus.core.seal import FanusSeal


def test_whitespace_only_seal_is_invalid():
    """F-36 regression: previously len(raw_text) > 0 passed whitespace-only text."""
    seal = FanusSeal("   ")
    assert seal.is_valid is False


def test_malformed_xml_falls_back_to_raw_and_is_invalid():
    """F-36 regression: XML-like input that fails to parse should not be
    silently accepted as a valid seal (previous check could never fail here)."""
    seal = FanusSeal("<unclosed>tag")
    assert seal.is_valid is False


def test_valid_plain_text_still_passes():
    seal = FanusSeal("test content")
    assert seal.is_valid is True


def test_valid_xml_seal_still_passes():
    seal = FanusSeal("<ONTOLOGY_PROTOCOL><VECTOR_CORE>x</VECTOR_CORE></ONTOLOGY_PROTOCOL>")
    assert seal.is_valid is True


def test_hash_is_always_valid_length_but_no_longer_sole_criterion():
    """The tautological check (hash length == 128) is always true for any
    SHA3-512 output -- confirms it alone is insufficient, which is why
    F-36 added the additional structural checks above."""
    seal = FanusSeal("   ")
    assert len(seal.hash) == 128
    assert seal.is_valid is False
