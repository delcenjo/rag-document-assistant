import numpy as np

from ragassistant.vector_store import VectorStore


def test_search_orders_by_cosine_similarity():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0], [0.7071, 0.7071]], dtype=np.float32)
    chunks = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    results = VectorStore(vectors, chunks).search(np.array([1.0, 0.0], dtype=np.float32), top_k=2)
    assert [chunk["id"] for chunk, _ in results] == ["a", "c"]


def test_save_and_load_roundtrip(tmp_path):
    vectors = np.eye(3, dtype=np.float32)
    chunks = [{"id": str(i)} for i in range(3)]
    VectorStore(vectors, chunks).save(tmp_path / "index.npz", tmp_path / "chunks.json")
    loaded = VectorStore.load(tmp_path / "index.npz", tmp_path / "chunks.json")
    assert loaded.chunks == chunks
    assert np.allclose(loaded.vectors, vectors)
