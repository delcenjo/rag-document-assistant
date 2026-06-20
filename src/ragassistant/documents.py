from .config import CHUNK_OVERLAP, CHUNK_SIZE


def load_documents(corpus_dir):
    documents = []
    for path in sorted(corpus_dir.glob("*.md")):
        documents.append({"source": path.name, "text": path.read_text(encoding="utf-8")})
    return documents


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current = [], ""
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 1 > chunk_size:
            chunks.append(current)
            current = (current[-overlap:] + " " + paragraph) if overlap else paragraph
        else:
            current = f"{current}\n{paragraph}".strip() if current else paragraph
    if current:
        chunks.append(current)
    return chunks


def build_chunks(documents, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    for document in documents:
        for i, text in enumerate(chunk_text(document["text"], chunk_size, overlap)):
            chunks.append({"id": f"{document['source']}#{i}", "source": document["source"], "text": text})
    return chunks
