from fastapi.testclient import TestClient

from fanus.api.server import app

client = TestClient(app)


def test_endpoints_that_return_memory_content_require_auth():
    """F-50: these GET endpoints return stored ledger/graph content, which includes the
    messages sent to /chat, so they must not be readable without an API key."""
    for path in ["/memory", "/memory/ledger", "/memory/graph"]:
        status = client.get(path).status_code
        assert status in (401, 503), f"{path} is readable without an API key (HTTP {status})"
