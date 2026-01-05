# src/normalize.py

def normalize_attribute(attr: dict) -> str:
    """
    Convert an attribute dictionary into a single semantic text block.
    Works for both Legacy and Strategic attributes.
    """

    lines = []

    # Business meaning first
    definition = attr.get("definition", "").strip()
    if definition:
        lines.append(f"Definition: {definition}")
    
    # Attribute  name next
    name = attr.get("attribute_name", "").strip()
    if name:
        lines.append(f"Attribute Name: {name}")
    
    # Table context
    table = attr.get("table_name", "").strip()
    if table:
        lines.append(f"Table: {table}")

    # Technical details
    datatype = attr.get("datatype", "").strip()
    if datatype:
        lines.append(f"Datatype: {datatype}")

    # pattern = attr.get("pattern", "").strip()
    # if pattern:
    #     lines.append(f"Pattern: {pattern}")

    # Strategic-only context (safe to ignore if missing)
    schema = attr.get("schema_name", "").strip()
    if schema:
        lines.append(f"Schema: {schema}")



    # source = attr.get("source_system", "").strip()
    # if source:
    #     lines.append(f"Source System: {source}")

    return "\n".join(lines)

## Test section only - will be removed in production

# sample = {
#     "attribute_name": "CUSTOMER_ID",
#     "definition": "Unique identifier for a customer",
#     "datatype": "VARCHAR(20)",
#     "schema_name": "FINANCE",
#     "table_name": "CUSTOMER"
# }

# print(normalize_attribute(sample))