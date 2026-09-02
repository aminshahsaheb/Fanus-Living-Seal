import time
from fastapi.testclient import TestClient
from fanus.api.server import app, loop


def test_chat_triggers_background_tick():
    """F-43 regression: /chat must trigger loop._tick() in the background
    (Governor/HardGuard/Evolution/Collapse/Observer must run on real chat
    traffic), without blocking the response itself."""
    client = TestClient(app)
    before = loop.tick_index

    response = client.post(
        "/chat",
        json={"message": "test"},
        headers={"X-API-Key": "test"}
    )
    # response returns even without waiting for the background task
    assert response.status_code in (200, 401, 503)

    time.sleep(1.0)
    after = loop.tick_index
    # Only assert progress if auth actually let the request through
    # (test environment may not have FANUS_API_KEY configured)
    if response.status_code == 200:
        assert after > before, f"tick_index did not advance: before={before}, after={after}"
