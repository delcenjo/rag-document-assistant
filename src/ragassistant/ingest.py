from .config import CORPUS_DIR, INDEX_PATH, META_PATH
from .documents import build_chunks, load_documents
from .embeddings import embed
from .vector_store import VectorStore


def main():
    documents = load_documents(CORPUS_DIR)
    chunks = build_chunks(documents)
    vectors = embed([chunk["text"] for chunk in chunks])
    VectorStore(vectors, chunks).save(INDEX_PATH, META_PATH)
    print(f"Indexed {len(chunks)} chunks from {len(documents)} documents -> {INDEX_PATH}")


if __name__ == "__main__":
    main()
