def test_health_returns_service_breakdown(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in ("ok", "degraded")
    assert set(body["services"].keys()) == {"postgres", "qdrant", "ollama"}
