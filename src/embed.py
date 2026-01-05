# src/embed.py

from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Wrapper around sentence-transformers embedding model.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def embed_text(self, text: str) -> list[float]:
        """
        Generate embedding for a single text string.
        """
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text")

        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()


## Test section only - will be removed in production

# embedder = EmbeddingModel()

# text = """
# Attribute Name: CUSTOMER_ID
# Definition: Unique identifier for a customer
# Datatype: VARCHAR(20)
# """

# vec = embedder.embed_text(text)

# print(len(vec))
# print(vec[:5])
