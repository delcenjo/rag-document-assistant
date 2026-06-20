import json

import numpy as np


class VectorStore:
    """In-memory cosine-similarity store backed by normalized embeddings."""

    def __init__(self, vectors=None, chunks=None):
        self.vectors = vectors
        self.chunks = chunks or []

    def search(self, query_vector, top_k):
        scores = self.vectors @ query_vector
        order = np.argsort(scores)[::-1][:top_k]
        return [(self.chunks[i], float(scores[i])) for i in order]

    def save(self, index_path, meta_path):
        index_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(index_path, vectors=self.vectors)
        meta_path.write_text(json.dumps(self.chunks, indent=2))

    @classmethod
    def load(cls, index_path, meta_path):
        vectors = np.load(index_path)["vectors"]
        chunks = json.loads(meta_path.read_text())
        return cls(vectors, chunks)
