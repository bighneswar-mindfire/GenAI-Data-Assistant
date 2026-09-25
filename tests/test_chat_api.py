import pytest


def test_chat_rejects_invalid_body(client):
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 422


@pytest.fixture(scope="module")
def ingested_refund_policy(client, live_services_available):
    if not live_services_available:
        pytest.skip("Ollama/Qdrant/Postgres not reachable — skipping live integration test")

    with open("data/documents/refund_policy.md", "rb") as f:
        response = client.post(
            "/documents/ingest",
            files={"file": ("refund_policy.md", f, "text/markdown")},
        )
    assert response.status_code == 200
    doc_id = response.json()["id"]

    yield doc_id

    client.delete(f"/documents/{doc_id}")


def test_chat_document_route_answers_from_policy(client, ingested_refund_policy):
    response = client.post("/chat", json={"message": "What is the refund policy?"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert "refund_policy.md" in body["sources"]


def test_chat_sql_route_answers_from_database(client, live_services_available):
    if not live_services_available:
        pytest.skip("Ollama/Qdrant/Postgres not reachable — skipping live integration test")

    response = client.post("/chat", json={"message": "Which are the top 5 customers by revenue?"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"]


def test_chat_combined_route_uses_both_sources(client, ingested_refund_policy):
    response = client.post(
        "/chat",
        json={"message": "What is the refund policy and how much was refunded last month?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert "refund_policy.md" in body["sources"]


def test_chat_follow_up_uses_session_history(client, live_services_available):
    if not live_services_available:
        pytest.skip("Ollama/Qdrant/Postgres not reachable — skipping live integration test")

    first = client.post("/chat", json={"message": "What is Alice Johnson's total revenue?"})
    assert first.status_code == 200
    session_id = first.json()["session_id"]

    second = client.post(
        "/chat",
        json={"message": "What did she buy?", "session_id": session_id},
    )
    assert second.status_code == 200
    assert second.json()["session_id"] == session_id
