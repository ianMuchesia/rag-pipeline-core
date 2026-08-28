# rag-pipeline-core

A from-scratch implementation of a **Retrieval-Augmented Generation (RAG) pipeline** — built piece by piece, starting from document chunking and embedding-based retrieval.

Same approach as the other projects: implement the components, understand why each decision was made, document what you learn. Project is ongoing.

---

## Core Pipeline

```
Raw Documents
      ↓
Document Loading
      ↓
Chunking
      ↓
Embedding Generation
      ↓
Vector Storage
      ↓
Similarity Search
      ↓
Top-K Relevant Chunks
```

Given a query like `"What is Kubernetes?"`, the system returns the most relevant document chunks based on embedding similarity.


## Project Structure

| Path | Contents |
| :--- | :--- |
| `src/document_processor.py` | Document loading and chunking strategies |
| `notebooks/` | Experiments and retrieval comparisons |
| `data/` | Sample document sets for testing |
| `experiments/` | Chunking strategy comparison results |
| `math-notes/` | Notes on embedding math and similarity metrics |

---

## Running

```bash
python -m venv venv && source venv/bin/activate
pip install sentence-transformers numpy
```

---

## Study Notes
See [NOTES.md](NOTES.md) for conceptual notes on chunking strategies, embedding similarity, and retrieval design decisions.
