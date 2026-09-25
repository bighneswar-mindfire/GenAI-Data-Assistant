import io


def test_list_documents_returns_a_list(client):
    response = client.get("/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_ingest_rejects_unsupported_extension(client):
    response = client.post(
        "/documents/ingest",
        files={"file": ("malware.exe", io.BytesIO(b"not a real file"), "application/octet-stream")},
    )
    assert response.status_code == 400


def test_ingest_rejects_empty_file(client):
    response = client.post(
        "/documents/ingest",
        files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")},
    )
    assert response.status_code == 400


def test_ingest_rejects_oversized_file(client):
    oversized = io.BytesIO(b"x" * (21 * 1024 * 1024))
    response = client.post(
        "/documents/ingest",
        files={"file": ("big.txt", oversized, "text/plain")},
    )
    assert response.status_code == 413


def test_delete_nonexistent_document_returns_404(client):
    response = client.delete("/documents/does-not-exist")
    assert response.status_code == 404
