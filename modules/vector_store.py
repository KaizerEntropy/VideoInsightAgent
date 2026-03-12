from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_vector_store(chunks):

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, chunks

def retrieve(query, index, chunks, k=3):

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, k)

    results = [chunks[i] for i in indices[0]]

    return results