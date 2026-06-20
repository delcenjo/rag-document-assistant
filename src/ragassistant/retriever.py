from .config import INDEX_PATH, META_PATH, TOP_K
from .embeddings import embed
from .vector_store import VectorStore


class Retriever:
    def __init__(self):
        self.store = VectorStore.load(INDEX_PATH, META_PATH)

    def retrieve(self, query, top_k=TOP_K):
        query_vector = embed([query])[0]
        return self.store.search(query_vector, top_k)
