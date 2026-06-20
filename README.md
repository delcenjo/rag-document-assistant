# RAG Document Assistant

A retrieval-augmented generation (RAG) assistant that answers natural-language
questions about a collection of documents and cites its sources. The included
corpus is the documentation of a fictional product (*Nimbus Notes*), so the
pipeline is fully runnable out of the box.

## How it works

```
documents → chunking → embeddings → vector store
                                          │
                       question → embedding → similarity search → top-k chunks
                                                                      │
                                                  prompt + context → Claude → answer
```

1. **Ingestion** — Markdown documents are split into overlapping chunks and
   embedded with a `sentence-transformers` model.
2. **Storage** — embeddings are kept in a small cosine-similarity vector store
   (NumPy) persisted to disk. It is intentionally transparent; in production it
   would be swapped for Chroma, Qdrant or pgvector behind the same interface.
3. **Retrieval** — the question is embedded and the most similar chunks are
   returned with their similarity scores.
4. **Generation** — the retrieved chunks are passed to Claude, which answers
   strictly from the context and cites the source filenames.

Retrieval and evaluation run completely offline. Generation needs an
`ANTHROPIC_API_KEY` (see `.env.example`).

## Project structure

```
src/ragassistant/
  config.py        paths, model names, chunking parameters
  documents.py     loading and chunking
  embeddings.py    sentence-transformers wrapper
  vector_store.py  cosine-similarity store with save/load
  ingest.py        build the index from the corpus
  retriever.py     embed a query and fetch top-k chunks
  generator.py     build the prompt and call Claude
  rag.py           retrieve + generate pipeline
  evaluate.py      retrieval recall@k on a labelled question set
  cli.py           ask questions from the command line
data/corpus/       the document collection
tests/             unit tests for chunking and the vector store
```

## Usage

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

python -m ragassistant.ingest                       # build the index
python -m ragassistant.evaluate                     # retrieval recall@k
python -m ragassistant.cli "How much does Pro cost?" --show-context
pytest
```

## Results

The corpus indexes into 10 chunks across 5 documents. On a labelled set of 8
questions, retrieval reaches **recall@4 = 0.88** (7/8) — the relevant document
appears in the top 4 results for all but one question.

Example for *"How much does the Pro plan cost and what storage does it include?"*:

```
[pricing.md]  score=0.550
[pricing.md]  score=0.480
[security.md] score=0.306
[faq.md]      score=0.242
```

The single miss ("Is Nimbus Notes SOC 2 compliant?") is a vocabulary-mismatch
case where the relevant chunk ranks just outside the top 4. It is exactly the
situation a cross-encoder re-ranking step or hybrid (dense + keyword) search is
designed to fix — see *Possible improvements*.

## Possible improvements

- Hybrid search (dense + BM25) and a cross-encoder re-ranking step.
- Streaming answers and conversation memory.
- Answer-level evaluation (faithfulness / groundedness) with an LLM judge.
