# src/output_writer.py

import pandas as pd
from pathlib import Path


def write_results(results: list[dict], output_path: str):
    """
    Write mapping results to an Excel file.
    """

    if not results:
        raise ValueError("No results to write")

    rows = []

    for r in results:
        rows.append({
            "Legacy Schema": r.get("legacy_schema"),
            "Legacy Table": r.get("legacy_table"),
            "Legacy Attribute": r.get("legacy_attribute"),
            "Primary Strategic Match": r.get("primary_match"),
            "Primary Similarity (%)": r.get("primary_similarity_pct"),
            "Strategic Table": r.get("strategic_table"),
            "Alternate Matches": ", ".join(r.get("alternates", [])),
            "Confidence": r.get("confidence"),
            "Reasoning": r.get("reasoning")
        })

        # rows.append({
        #     "legacy_table_name": r.get("legacy_schema") + "." + r.get("legacy_table"),
        #     "Legacy/Conformance Attribute": r.get("legacy_attribute"),
        #     "Primary CDM Matched Field": r.get("primary_match"),
        #     "Primary CDM Matched Table": r.get("table_name"),
        #     "Alternate Matches": ", ".join(r.get("alternates", [])),
        #     "Confidence": r.get("confidence"),
        #     "Reasoning": r.get("reasoning")
        # })

    df = pd.DataFrame(rows)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_excel(output_path, index=False)

    print(f"Results written to: {output_path}")

## Test section only - will be removed in production

# results = [
#     {
#         "legacy_attribute": "CLIENT_ID",
#         "primary_match": "CUSTOMER_ID",
#         "legacy_table": "ENTITIES",
#         "legacy_schema": "RAW_DATA",
#         "schema_name" : "WAREHOUSE",
#         "table_name": "ACCOUNTS",
#         "alternates": ["ORDER_ID"],
#         "confidence": "High",
#         "reasoning": "Both represent unique identifiers for customers."
#     }
# ]

# write_results(results, "data/output/Probable_Mapping_Results.xlsx")