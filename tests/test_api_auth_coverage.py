from fastapi.testclient import TestClient
from fanus.api.server import app

client = TestClient(app)

AUTH_REQUIRED_ENDPOINTS = [
    ("/chat", {"message": "test"}),
    ("/verify", {"prompt": "test", "response": "test", "context": ""}),
    ("/verify/deep", {"prompt": "test", "response": "test"}),
    ("/memory/store", {"content": "test", "source": "test"}),
    ("/memory/version", {"key": "test", "content": "test"}),
    ("/decision/goal", {"goal": "test"}),
    ("/decision/plan", {"vision": "test", "milestones": []}),
    ("/auto/research", {"topic": "test"}),
    ("/research/plan", {"topic": "test"}),
    ("/research/search", {"query": "test"}),
    ("/reason/analyze", {"text": "test"}),
    ("/reason/contradict", {"claim_a": "a", "claim_b": "b"}),
    ("/reason/hypothesize", {"topic": "test"}),
    ("/knowledge/search", {"query": "test"}),
    ("/knowledge/validate", {"claim": "test"}),
]


def test_all_mutating_endpoints_require_auth():
    """F-29 full coverage: every mutating POST endpoint must reject requests without a valid API key."""
    failures = []
    for path, body in AUTH_REQUIRED_ENDPOINTS:
        r = client.post(path, json=body)
        if r.status_code not in (401, 503):
            failures.append((path, r.status_code))
    assert not failures, f"Endpoints missing auth enforcement: {failures}"
