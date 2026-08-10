from fastapi.testclient import TestClient
from fanus.api import auth


def test_no_keys_configured_denies_all(monkeypatch):
    """F-29 regression: missing FANUS_API_KEY must deny, not fail-open."""
    monkeypatch.setattr(auth, "VALID_KEYS", set())
    import pytest
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        auth.verify_api_key(api_key=None)
    assert exc.value.status_code == 503


def test_correct_key_passes(monkeypatch):
    monkeypatch.setattr(auth, "VALID_KEYS", {"secret123"})
    result = auth.verify_api_key(api_key="secret123")
    assert result is True


def test_wrong_key_denied(monkeypatch):
    monkeypatch.setattr(auth, "VALID_KEYS", {"secret123"})
    import pytest
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        auth.verify_api_key(api_key="wrong")
    assert exc.value.status_code == 401
