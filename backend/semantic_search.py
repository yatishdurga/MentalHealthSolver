import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load vector store from disk
with open("vector_store.pkl", "rb") as f:
    VECTOR_STORE = pickle.load(f)

def find_similar_statements(query_embedding, top_k=5):
    """
    Given a query embedding, return the top-k most similar statements.
    """
    # Extract just the embeddings from the vector store
    embeddings = np.array([entry["embedding"] for entry in VECTOR_STORE])

    # Compute cosine similarity
    similarities = cosine_similarity([query_embedding], embeddings)[0]

    # Get top k indices sorted by similarity
    top_indices = np.argsort(similarities)[::-1][:top_k]

    # Collect top k similar items
    results = []
    for idx in top_indices:
        results.append({
            "statement": VECTOR_STORE[idx]["statement"],
            "category": VECTOR_STORE[idx]["category"],
            "score": round(similarities[idx], 3)
        })
    return results
