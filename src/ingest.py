# src/ingest.py

import pandas as pd


# LEGACY_COLUMN_MAP = {
#     "Catalog_Schema Name": "schema_name",
#     "Table Name": "table_name",
#     "Column Name": "attribute_name",
#     "Column Type": "datatype",
#     "Column Description": "definition"
# }

STRATEGIC_COLUMN_MAP = {
    "Catalog_Schema Name": "schema_name",
    "Table Name": "table_name",
    "Column Name": "attribute_name",
    "Column Type": "datatype",
    "Column Description": "definition"
}

INPUT_TEMPLATE_COLUMN_MAP = {
    "System_Name": "system_name",
    "Report_Area": "report_area",
    "Report_Name": "report_name",
    "ECS+ File": "sor_src_file_name",
    "ECS Field Name": "sor_field_name",
    "Conformance Table": "table_name",
    "Conformance Field": "attribute_name",
    "Conformance_Datatype_Derived": "datatype",
    "Conformance_Description_Derived": "definition"
}


def _validate_columns(df: pd.DataFrame, required: set, file_name: str):
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"{file_name} is missing required columns: {missing}"
        )


# def load_legacy_dict(path: str) -> list[dict]:
#     """
#     Load Legacy data dictionary from Excel.
#     """
#     df = pd.read_excel(
#          path,
#          engine="xlrd",
#          nrows=250
#    )

#     _validate_columns(
#         df,
#         required=set(LEGACY_COLUMN_MAP.keys()),
#         file_name=path
#     )

#     # Select and rename only required columns
#     df = df[list(LEGACY_COLUMN_MAP.keys())]
#     df = df.rename(columns=LEGACY_COLUMN_MAP)

#     records = df.fillna("").to_dict(orient="records")
#     return records


def load_strategic_dict(path: str) -> list[dict]:
    """
    Load Strategic data dictionary from Excel.
    Only selected columns are ingested and renamed.
    """
    df = pd.read_excel(
         path,
         engine="xlrd"
   )

    _validate_columns(
        df,
        required=set(STRATEGIC_COLUMN_MAP.keys()),
        file_name=path
    )

    # Select and rename only required columns
    df = df[list(STRATEGIC_COLUMN_MAP.keys())]
    df = df.rename(columns=STRATEGIC_COLUMN_MAP)

    records = df.fillna("").to_dict(orient="records")
    return records


def load_mapping_template(path: str) -> list[dict]:
    """
    Load mapping template (Legacy attributes to be mapped).
    """
    df = pd.read_excel(
         path,
         engine="xlrd",
         nrows=5   ## limit for POC

   )

    _validate_columns(
        df,
        required={"Conformance Field", "Conformance Table"},
        file_name=path
    )
    
    # Select and rename only present columns
    present_columns = [col for col in INPUT_TEMPLATE_COLUMN_MAP.keys() if col in df.columns]
    df = df[present_columns]
    df = df.rename(columns=INPUT_TEMPLATE_COLUMN_MAP)

    records = df.fillna("").to_dict(orient="records")
    return records


## Test section only - will be removed in production

# print("Testing ingest module...")
# strategic = load_strategic_dict("data\input\Strategic_CDM_Dictionary.xls")
# print(strategic[0])
# # print(strategic[3])


# legacy = load_legacy_dict("data\input\Legacy_Conformance_Dictionary.xls")
# print(legacy[0])
# # print(legacy[2])

# inp_template = load_mapping_template("data\input\MainSearch_InputTemplate.xls")
# print(inp_template[0])
# #print(inp_template[2])

# print("testing succeeded......proceeding with next steps...")
