# src/retrieve.py
from src.embed import EmbeddingModel
from src.vector_store import StrategicVectorStore
from src.normalize import normalize_attribute


HIGH_CONFIDENCE_THRESHOLD = 0.75
MEDIUM_CONFIDENCE_THRESHOLD = 0.60


def retrieve_candidates(
    legacy_embedding: list[float],
    vector_store,
    top_k: int = 5
) -> list[dict]:
    """
    Retrieve and classify top candidate Strategic attributes.
    """

    raw_results = vector_store.search(
        query_embedding=legacy_embedding,
        top_k=top_k
    )

    candidates = []

    for result in raw_results:
        score = result["score"]
        metadata = result["metadata"]

        if score >= HIGH_CONFIDENCE_THRESHOLD:
            confidence = "High"
        elif score >= MEDIUM_CONFIDENCE_THRESHOLD:
            confidence = "Medium"
        else:
            confidence = "Low"

        candidates.append({
            "attribute_name": metadata.get("attribute_name"),
            "definition": metadata.get("definition"),
            "datatype": metadata.get("datatype"),
            "schema_name": metadata.get("schema_name", ""),
            "table_name": metadata.get("table_name", ""),
            "similarity_score": round(score, 3),
            "confidence": confidence
        })

    return candidates

## Test section only - will be removed in production


# strategic = [
#     {
#         "attribute_name": "CUSTOMER_ID",
#         "schema_name" : "WAREHOUSE",
#         "table_name": "ACCOUNTS",
#         "definition": "Unique identifier for a customer",
#         "datatype": "VARCHAR(20)"
#     },
#     {
#         "attribute_name": "ORDER_ID",
#         "schema_name" : "WAREHOUSE",
#         "table_name": "ORDERS",
#         "definition": "Unique identifier for an order",
#         "datatype": "VARCHAR(20)"
#     }
# ]

# for a in strategic:
#     a["normalized_text"] = normalize_attribute(a)

# embedder = EmbeddingModel()
# store = StrategicVectorStore(embedder.dimension)
# store.build_index(strategic, embedder)

# legacy = normalize_attribute({
#     "attribute_name": "GFC_ID",
#     "definition": "Accounting Identifier of the top level client"
# })

# legacy_vec = embedder.embed_text(legacy)

# candidates = retrieve_candidates(
#     legacy_embedding=legacy_vec,
#     vector_store=store,
#     top_k=2
# )

# for c in candidates:
#     print(c)
