from app.rag.chunking import chunk_text


def test_short_text_produces_one_chunk():
    chunks = chunk_text("This is a short sentence.")
    assert len(chunks) == 1


def test_long_text_splits_into_multiple_chunks():
    paragraph = "This is one sentence that repeats. " * 100
    chunks = chunk_text(paragraph)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 1000


def test_empty_text_produces_no_chunks():
    assert chunk_text("") == []
