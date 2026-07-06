import pytest
from fanus.core.seal import FanusSeal

def test_seal_hash():
    s = FanusSeal("test content")
    assert len(s.hash) == 128

def test_seal_valid():
    s = FanusSeal("test content")
    assert s.is_valid == True

def test_seal_xml():
    s = FanusSeal("<ONTOLOGY_PROTOCOL><VECTOR_CORE>core</VECTOR_CORE></ONTOLOGY_PROTOCOL>")
    assert "VECTOR_CORE" in s.layers
