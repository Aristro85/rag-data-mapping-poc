# src/llm_reasoner.py

import json
import requests


# OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def _build_prompt(legacy_text: str, candidates: list[dict]) -> str:
    """
    Build a structured prompt for the LLM.
    """

    candidate_text = ""
    for idx, c in enumerate(candidates, start=1):
        candidate_text += (
            f"\nCandidate {idx}:\n"
            f"Name: {c['attribute_name']}\n"
            f"Definition: {c['definition']}\n"
            f"Datatype: {c['datatype']}\n"
            f"Similarity Score: {c['similarity_score']}\n"
        )

    prompt = f"""
You are a data migration expert assisting with attribute mapping from legacy systems to a strategic data model.

Legacy Attribute:
{legacy_text}

Strategic Attribute Candidates:
{candidate_text}

TASK:
1. Select the best primary match.
2. Rank remaining candidates as alternates.
3. Explain briefly why the primary match was chosen.

RULES:
- Base your decision on semantic and contextual meaning, not just names.
- If no candidate is a good match, still choose the best available.
- Respond ONLY in valid JSON.
- Do not include explanations, markdown, or extra text.
- Do not wrap the JSON in backticks.

JSON FORMAT:
{{
  "primary_match": "<attribute_name>",
  "primary_index": <number>,
  "confidence": "High | Medium | Low",
  "reasoning": "<short explanation>"
}}
"""
    return prompt.strip()


def reason_over_candidates(
    legacy_text: str,
    candidates: list[dict],
    model_name: str = "gemma3:1b"
    #model_name: str = "deepseek-r1:8b"     ## this is way better, but significantly slower
) -> dict:
    """
    Call Ollama LLM to reason over retrieved candidates.
    """

    if not candidates:
        return {
            "primary_match": None,
            "primary_index": 0,
            #"alternates": [],
            "confidence": "Low",
            "reasoning": "No candidates retrieved"
        }

    prompt = _build_prompt(legacy_text, candidates)

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=360)
    response.raise_for_status()

    raw_output = response.json().get("response", "").strip()
    print("RAW LLM OUTPUT:\n", raw_output)

    try:
        result = json.loads(raw_output)
    except json.JSONDecodeError:
        # Safe fallback if model misbehaves
        result = {
            "primary_match": candidates[0]["attribute_name"],
            "primary_index": 0,
            "schema_name": candidates[0]["schema_name"],
            "table_name": candidates[0]["table_name"],
            # "alternates": [c["attribute_name"] for c in candidates[1:]],
            "confidence": candidates[0]["confidence"],
            "reasoning": "LLM output could not be parsed; fallback used"
        }

    return result

## Test section only - will be removed in production

# test_llm_reasoner.py

# legacy_text = """
# Attribute Name: CLIENT_ID
# Definition: Unique identifier for a corporate client customer
# Datatype: VARCHAR(20)
# """

# candidates = [
#     {
#         "attribute_name": "CUSTOMER_ID",
#         "definition": "Unique identifier for a customer",
#         "datatype": "VARCHAR(20)",
#         "similarity_score": 0.78,
#         "confidence": "High"
#     },
#     {
#         "attribute_name": "ORDER_ID",
#         "definition": "Unique identifier for an order",
#         "datatype": "VARCHAR(20)",
#         "similarity_score": 0.42,
#         "confidence": "Low"
#     }
# ]

# result = reason_over_candidates(
#     legacy_text=legacy_text,
#     candidates=candidates,
#     model_name: str = "gemma3:1b"
#     #model_name: str = "deepseek-r1:8b"     ## this is way better, but significantly slower
# )

# print(result)
