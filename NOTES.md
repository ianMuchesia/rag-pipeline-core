# Notes: RAG Pipeline Core

## 1. Sentence Chunking — Three Engineering Details That Matter

**Accounting for spaces when measuring chunk length:**
When calculating `current_length`, you must account for the spaces that join sentences back into a single string. Five sentences require four space characters between them. Ignoring this means the actual chunk silently exceeds the size limit — which can cause downstream failures if the embedding model has strict input limits. Fix: add `+1` to `current_length` for each sentence appended.

**The empty chunk guard (`and current_chunk`):**
The `if` condition includes `and current_chunk` to handle a specific edge case: a single massive sentence (e.g. 300 characters) that exceeds the limit on the very first iteration. Without this guard, an empty chunk would immediately trigger a split, producing an empty first chunk and a second chunk starting with that same massive sentence. With the guard, the massive sentence bypasses the trigger, gets appended, and forces a new chunk on the next iteration — the soft limit approach.

**Output must be a list of strings, not a list of lists:**
Vector databases and embedding models expect raw text strings as input. Before appending `current_chunk` to `final_chunks`, apply `" ".join(current_chunk)` to flatten the sentence list back into paragraph format.

**The trailing chunk bug:**
When the for loop runs out of sentences, it appends the last sentence to `current_chunk` and terminates. The size limit condition never triggers on the final group, so those sentences never get appended to `final_chunks`. Always add a cleanup step after the loop:
```python
if current_chunk:
    final_chunks.append(" ".join(current_chunk))
```

## 2. The Soft Limit vs Hard Limit Problem
When a single sentence is longer than the target chunk size (e.g. limit is 200 chars, sentence is 300 chars), you're forced to break a rule. Two approaches:

- **Soft Limit (most common):** let that specific chunk be oversized. Put the giant sentence in its own chunk. Modern embedding models and vector databases have enough headroom to handle a chunk slightly over the target.
- **Hard Limit (fallback):** if you absolutely cannot exceed the limit (strict memory constraints), fall back to fixed-size chunking for just that one sentence — accept the unnatural mid-sentence break.

Soft limit is the default for most real-world RAG systems.

## 3. Chunk Overlap — What It Actually Is
Overlap is not a hidden character or separator. It's literally copy-pasting the last N sentences of the previous chunk so they appear at the start of the next chunk.

**Why this matters — the pronoun problem:**
Without overlap:
```
Chunk 1: "Apple released a new phone today."
Chunk 2: "It has a better camera." "The battery lasts 24 hours."
```
A query for "which Apple phone has a better camera?" hits Chunk 2, which contains "better camera" — but only says "It". No idea what "It" refers to. The search fails.

With 1-sentence overlap:
```
Chunk 1: "Apple released a new phone today."
Chunk 2: "Apple released a new phone today." "It has a better camera." "The battery lasts 24 hours."
```
Chunk 2 now contains both "Apple" and "better camera" in the same vector. The retrieval succeeds.

**What if the sentences aren't related?** Copy-pasting an unrelated sentence just adds a tiny bit of harmless clutter to the next chunk. When they are related (pronouns, references), it saves the entire retrieval from failing. It's an insurance policy — cheap when it's unnecessary, critical when it's needed.