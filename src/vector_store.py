# src/vector_store.py

import faiss
import numpy as np
from src.embed import EmbeddingModel
from src.normalize import normalize_attribute

class StrategicVectorStore:
    """
    FAISS-based vector store for Strategic attributes.
    """

    def __init__(self, embedding_dim: int):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.metadata = []


    def build_index(self, strategic_attrs: list[dict], embedder):
        """
        Build FAISS index from Strategic attributes.
        """
        embeddings = []

        for attr in strategic_attrs:
            text = attr.get("normalized_text")
            if not text:
                continue

            vector = embedder.embed_text(text)
            embeddings.append(vector)
            self.metadata.append(attr)

        if not embeddings:
            raise ValueError("No embeddings generated for Strategic attributes")

        vectors_np = np.array(embeddings).astype("float32")
        self.index.add(vectors_np)

    def search(self, query_embedding: list[float], top_k: int = 5):
        """
        Search FAISS index and return top-k matches.
        """
        if self.index.ntotal == 0:
            raise ValueError("FAISS index is empty")

        query_np = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(query_np, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            results.append({
                "score": float(score),
                "metadata": self.metadata[idx]
            })

        return results

## Test section only - will be removed in production



# strategic = [
#     {
#         "attribute_name": "CUSTOMER_ID",
#         "definition": "Unique identifier for a customer",
#         "datatype": "VARCHAR(20)"
#     },
#     {
#         "attribute_name": "ORDER_ID",
#         "definition": "Unique identifier for an order",
#         "datatype": "VARCHAR(20)"
#     }
# ]

# for a in strategic:
#     a["normalized_text"] = normalize_attribute(a)

# embedder = EmbeddingModel()
# store = StrategicVectorStore(embedder.dimension)
# store.build_index(strategic, embedder)

# query = normalize_attribute({
#     "attribute_name": "GFC_ID",
#     "definition": "Accounting Identifier of the top level client"
# })

# query_vec = embedder.embed_text(query)
# results = store.search(query_vec, top_k=2)

# for r in results:
#     print(r["score"], r["metadata"]["attribute_name"])
