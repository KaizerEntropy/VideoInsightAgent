from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re


model = SentenceTransformer("all-MiniLM-L6-v2")


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())


def keyword_overlap_score(query: str, chunk: str) -> float:
    query_terms = set(normalize_text(query).split())
    chunk_terms = set(normalize_text(chunk).split())

    if not query_terms:
        return 0.0

    return len(query_terms & chunk_terms) / len(query_terms)


def create_vector_store(chunks):

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, chunks

def retrieve(query, index, chunks, k=5):
    if not chunks:
        return []

    query_embedding = model.encode([query])

    search_k = min(max(k * 3, k), len(chunks))
    distances, indices = index.search(query_embedding, search_k)

    reranked = []

    for distance, chunk_index in zip(distances[0], indices[0]):
        if chunk_index < 0:
            continue

        chunk = chunks[chunk_index]
        semantic_score = 1 / (1 + float(distance))
        lexical_score = keyword_overlap_score(query, chunk)
        combined_score = (semantic_score * 0.75) + (lexical_score * 0.25)
        reranked.append((combined_score, chunk))

    reranked.sort(key=lambda item: item[0], reverse=True)

    results = []

    for _, chunk in reranked:
        if chunk not in results:
            results.append(chunk)
        if len(results) == k:
            break

    return results
