from ragassistant.documents import build_chunks, chunk_text


def test_chunk_text_splits_long_text():
    text = "\n\n".join("paragraph text here " * 10 for _ in range(6))
    chunks = chunk_text(text, chunk_size=300, overlap=0)
    assert len(chunks) > 1


def test_chunk_text_keeps_short_text_in_one_chunk():
    assert chunk_text("short text", chunk_size=600, overlap=50) == ["short text"]


def test_build_chunks_assigns_source_and_id():
    documents = [{"source": "a.md", "text": "one\n\ntwo"}]
    chunks = build_chunks(documents, chunk_size=5, overlap=0)
    assert chunks[0]["source"] == "a.md"
    assert chunks[0]["id"].startswith("a.md#")
