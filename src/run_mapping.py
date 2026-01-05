# src/run_mapping.py

from src.ingest import (
    #load_legacy_dict,
    load_strategic_dict,
    load_mapping_template
)
from src.normalize import normalize_attribute
from src.embed import EmbeddingModel
from src.vector_store import StrategicVectorStore
from src.retrieve import retrieve_candidates
from src.llm_reasoner import reason_over_candidates
from src.output_writer import write_results


OUTPUT_PATH = "data/output/Probable_Mapping_Results.xlsx"
#LLM_MODEL = "gemma3:1b"   # fast & acceptable for POC
LLM_MODEL = "deepseek-r1:8b"   # fast & acceptable for POC
#LLM_MODEL = "phi3:3.8b"   # faster and better quality for POC, but lacks formatting capabilities
TOP_K = 2
PRIMARY_MATCH_THRESHOLD = 0.5
GAP_FLAG = "NO_GOOD_MATCH"



def main():
    print("Starting AI assisted RAG-based data mapping POC run...")

    # 1. Load input Excel files
    print(" Loading Excel inputs...")
    #legacy_attrs = load_legacy_dict("data\input\Legacy_Conformance_Dictionary.xls")
    strategic_attrs = load_strategic_dict("data\input\Strategic_CDM_Dictionary.xls")
    mapping_template = load_mapping_template("data\input\MainSearch_InputTemplate.xls")

    print(f"  No. of Legacy attributes: {len(mapping_template)}")
    print(f"  No. of Strategic attributes: {len(strategic_attrs)}\n")

    # Normalize Strategic attributes
    print(" Normalizing Strategic attributes...")
    for attr in strategic_attrs:
        attr["normalized_text"] = normalize_attribute(attr)

    # Initialize embedding + vector store
    print(" Initializing embedding model...")
    embedder = EmbeddingModel()

    print(" Building FAISS index (Strategic)...")
    vector_store = StrategicVectorStore(embedder.dimension)
    vector_store.build_index(strategic_attrs, embedder)

    results = []

    # Process each Legacy attribute
    print("\n Processing Legacy attributes...\n")

    for idx, legacy in enumerate(mapping_template, start=1):
        
        legacy_name = legacy.get("attribute_name")
        legacy_table = legacy.get("table_name")
        legacy_report = legacy.get("report_name")
        legacy_datatype = legacy.get("datatype")
        legacy_definition = legacy.get("definition")        
        print(f"[{idx}] Mapping Legacy attribute: {legacy_name}")

        legacy_text = normalize_attribute(legacy)
        legacy_embedding = embedder.embed_text(legacy_text)

        # Retrieve semantic candidates
        candidates = retrieve_candidates(
            legacy_embedding=legacy_embedding,
            vector_store=vector_store,
            top_k=TOP_K
        )

        # # LLM reasoning
        # llm_result = reason_over_candidates(
        #     legacy_text=legacy_text,
        #     candidates=candidates,
        #     model_name=LLM_MODEL
        # )

        # # Find schema_name and table_name for the primary match from candidates
        # primary_match_attr = llm_result.get("primary_match")
        # primary_schema = ""
        # primary_table = ""
        # if primary_match_attr:
        #     for cand in candidates:
        #         if cand.get("attribute_name") == primary_match_attr:
        #             primary_schema = cand.get("schema_name", "")
        #             primary_table = cand.get("table_name", "")
        #             break

        # results.append({
        #     "legacy_table": legacy_table,
        #     "legacy_schema": legacy_report,
        #     "legacy_attribute": legacy_name,
        #     "primary_match": llm_result["primary_match"],
        #     "table_name": f"{primary_schema}.{primary_table}" if primary_schema and primary_table else "",
        #     "alternates": llm_result["alternates"],
        #     "confidence": llm_result["confidence"],
        #     "reasoning": llm_result["reasoning"]
        # })
        
        # LLM reasoning
        llm_result = reason_over_candidates(
            legacy_text=legacy_text,
            candidates=candidates,
            model_name=LLM_MODEL
        )
        
        primary_schema = ""
        primary_table = ""
        primary_similarity_pct = None
        
        # Determine primary candidate
        primary_idx = llm_result.get("primary_index")
        
        if primary_idx is not None and primary_idx < len(candidates):
            primary_candidate = candidates[primary_idx]
        else:
            # fallback to attribute name match
            primary_match_attr = llm_result.get("primary_match")
            primary_candidate = next(
                (c for c in candidates if c.get("attribute_name") == primary_match_attr),
                None
            )
        
        # Extract primary match metadata
        if primary_candidate:
            primary_schema = primary_candidate.get("schema_name", "")
            primary_table = primary_candidate.get("table_name", "")
            primary_similarity_pct = round(
                primary_candidate.get("similarity_score", 0) * 100, 2
            )
        
        # Gap flagging
        if primary_candidate and primary_candidate.get("similarity_score", 0) < PRIMARY_MATCH_THRESHOLD:
            primary_match_name = "NO_GOOD_MATCH"
        else:
            primary_match_name = llm_result.get("primary_match")
        
        # Format alternates with similarity %
        alternate_matches = []
        for i, c in enumerate(candidates):
            if primary_candidate and c is primary_candidate:
                continue
            alt_score = round(c.get("similarity_score", 0) * 100, 2)
            alternate_matches.append(f"{c['attribute_name']} ({alt_score}%)")
        
        results.append({
            "legacy_schema": legacy_report,
            "legacy_table": legacy_table,
            "legacy_attribute": legacy_name,
            "primary_match": primary_match_name,
            "primary_similarity_pct": primary_similarity_pct,
            "strategic_table": (
                f"{primary_schema}.{primary_table}"
                if primary_schema and primary_table else ""
            ),
            "alternates": alternate_matches,
            "confidence": llm_result.get("confidence"),
            "reasoning": llm_result.get("reasoning")
        })

    # Write output Excel
    print("\nWriting final output Excel...")
    write_results(results, OUTPUT_PATH)

    print("\nMapping completed successfully!")
    print(f" Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()