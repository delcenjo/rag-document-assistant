# RAG Document Assistant

![CI](https://github.com/delcenjo/rag-document-assistant/actions/workflows/ci.yml/badge.svg)

This is a small retrieval-augmented generation assistant. You point it at a folder
of documents, ask a question in plain language, and it answers using only what it
found in those documents, citing the files it pulled the answer from. The repo
ships with the documentation of a made-up product called *Nimbus Notes*, so you can
clone it and get a working pipeline without supplying any data of your own.

The whole thing is deliberately compact. The vector store is a few lines of NumPy
rather than a hosted database, and each step lives in its own short module, so the
moving parts of RAG are easy to read end to end.

## The pipeline, start to finish

RAG splits into two halves: finding the right text (retrieval), and turning that
text into an answer (generation). Retrieval is the part that actually runs here
out of the box; generation is one API call you can switch on whenever you have a key.

**Retrieval** begins with indexing. `ingest.py` loads every Markdown file under
`data/corpus/`, and `documents.py` breaks each one into overlapping chunks (paragraph
by paragraph, roughly 600 characters with 100 characters of overlap so a thought
isn't cut cleanly in two). Each chunk is embedded with a `sentence-transformers`
model (`all-MiniLM-L6-v2`) in `embeddings.py`, and the resulting vectors plus their
chunk metadata are saved to `storage/` by the `VectorStore` in `vector_store.py`.

When a question comes in, `retriever.py` embeds it with the same model and asks the
store for the closest chunks. Because the embeddings are normalized, "closest" is
just a dot product, which is cosine similarity, sorted descending. You get back the
top few chunks together with their scores.

**Generation** is where an LLM enters. `generator.py` stitches the retrieved chunks
into a context block, prepends a system prompt that tells the model to answer strictly
from that context (and to say it doesn't know otherwise), and sends it off. The
prompt also asks the model to cite each fact with its source filename in square
brackets. `rag.py` ties retrieval and generation together into a single `answer()` call.

## Trying it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

python -m ragassistant.ingest     # build the index from data/corpus
python -m ragassistant.evaluate   # check retrieval quality
python -m ragassistant.cli "How much does the Pro plan cost?" --show-context
pytest
```

The CLI works with no key at all: it will print the chunks it retrieved and their
scores. To get a written answer, copy `.env.example` to `.env` and add a key for an
LLM API (an LLM API key); without one, the CLI just tells you that generation is
off and shows the retrieved context instead. Indexing, search, and evaluation never
need a key.

A run with `--show-context` looks roughly like this:

```
Retrieved context:
  [pricing.md]  score=0.550
  [pricing.md]  score=0.480
  [security.md] score=0.306
  [faq.md]      score=0.242
```

The two `pricing.md` chunks land on top for a pricing question, which is what you want.

## How well retrieval does

The sample corpus indexes into 10 chunks across 5 documents. `evaluate.py` runs a
hand-labelled set of 8 questions and measures recall@4: for how many questions does
the correct source document show up in the top 4 results. On this set it scores 0.88,
or 7 out of 8.

The one it misses is "Is Nimbus Notes SOC 2 compliant?". The right chunk is there but
ranks just past the cutoff, a classic case of the question and the document wording
not overlapping much. Dense embeddings alone struggle with that; a keyword signal or
a re-ranking pass would be the natural fix.

## Layout

```
src/ragassistant/
  config.py        paths, model names, chunk size and top-k
  documents.py     loading files and splitting them into chunks
  embeddings.py    sentence-transformers wrapper
  vector_store.py  cosine-similarity store with save/load
  ingest.py        builds the index from the corpus
  retriever.py     embeds a query, returns the top-k chunks
  generator.py     builds the prompt and calls the LLM
  rag.py           retrieve-then-generate pipeline
  evaluate.py      recall@k over the labelled question set
  cli.py           ask questions from the terminal
data/corpus/       the Nimbus Notes documents
tests/             chunking and vector-store unit tests
```

## Notes on scope

The vector store is intentionally plain. It keeps everything in memory and on disk as
a NumPy array plus a JSON file, which is fine for a corpus this size and easy to inspect.
For anything larger you would put Chroma, Qdrant, or pgvector behind the same small
interface and leave the rest untouched.

The obvious next steps, if this were to grow, are adding a keyword signal alongside the
dense search (and a re-ranking step) to catch cases like the SOC 2 miss, streaming the
generated answer, and scoring answer quality rather than just retrieval.
