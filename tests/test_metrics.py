import importlib
from fastapi.testclient import TestClient


def test_metrics_enabled(monkeypatch):
    monkeypatch.setenv("ENABLE_MONITORING", "true")
    import app.metrics as metrics
    importlib.reload(metrics)
    import app.api.main as main
    importlib.reload(main)
    client = TestClient(main.app)
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "processed_messages_total" in resp.text
