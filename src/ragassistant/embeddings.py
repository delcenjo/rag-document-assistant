from functools import lru_cache

import numpy as np

from .config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL)


def embed(texts):
    vectors = _model().encode(
        list(texts), normalize_embeddings=True, convert_to_numpy=True
    )
    return np.asarray(vectors, dtype=np.float32)
