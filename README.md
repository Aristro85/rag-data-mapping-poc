***** README *****

Step1: Initial Env setup: 
------------------------------------------------------------------------------------------------
In Command line or VS-Code Terminal, run these to setup the initial Venv: 


cd C:\Users\arist\genai_training\vscodestuff\MAP_POC\rag-data-mapping-poc
C:\Users\arist\genai_training\vscodestuff\MAP_POC\rag-data-mapping-poc> py -3.11 -m venv myenv
C:\Users\arist\genai_training\vscodestuff\MAP_POC\rag-data-mapping-poc> venv\Scripts\activate

(myenv) C:\Users\arist\genai_training\vscodestuff\MAP_POC\rag-data-mapping-poc> pip install pandas openpyxl faiss-cpu sentence-transformers requests
(myenv) C:\Users\arist\genai_training\vscodestuff\MAP_POC\rag-data-mapping-poc> python.exe -m pip install --upgrade pip
(myenv) C:\Users\arist\genai_training\vscodestuff\MAP_POC\rag-data-mapping-poc> pip install langchain langchain-community langchain-ollama



Step2: Check LLM imports and other packages for completion: 
----------------------------------------------------------------------------------------------------------------------------
cd C:\Users\arist\genai_training\vscodestuff\MAP_POC\rag-data-mapping-poc
venv\Scripts\activate
python -m src.main




Step3: If Above step works fine, you are able to setup all the right packages 
to call LLM (gemma3:1b) locally. Then you can proceed with running the
mapping gap analysis using the below command: 
----------------------------------------------------------------------------------------------------------------------------
(venv) C:\Users\arist\genai_training\vscodestuff\MAP_POC\rag-data-mapping-poc>python -m src.run_mapping




>> Typical output is shown below: 
----------------------------------------------------------------------------------------------------------------------------

Starting AI assisted RAG-based data mapping POC run...
 Loading Excel inputs...
  No. of Legacy attributes: 3
  No. of Strategic attributes: 719

 Normalizing Strategic attributes...
 Initializing embedding model...
 Building FAISS index (Strategic)...

 Processing Legacy attributes...

[1] Mapping Legacy attribute: ACCT_BILL_TYP_COD
RAW LLM OUTPUT:
 ```json
{
  "primary_match": "ACCOUNT_CASHACCOUNTSERVICE_BILLINGCHARGEMETHOD",
  "alternates": ["STATEMENT_CASHACCOUNTSERVICE_BILLINGCHARGEMETHOD"],
  "confidence": "Medium",
  "reasoning": "The strategic attributes describe billing methods (individually or centrally billed), which aligns with the legacy attribute's purpose of indicating account billing type, despite the legacy attribute having three categories while the candidates only mention two."
}
```
[2] Mapping Legacy attribute: ACCT_CUST_NO
RAW LLM OUTPUT:
 ```json
{
  "primary_match": "ACCOUNT_ACCOUNTIDENTIFICATION_NUMBER",
  "alternates": ["ACCOUNT_FIRST_ACCOUNT_NUMBER"],
  "confidence": "Medium",
  "reasoning": "The definition of ACCOUNT_ACCOUNTIDENTIFICATION_NUMBER aligns closely with the legacy attribute's purpose as a unique identifier, despite a moderate name similarity score. The alternative candidate has a slightly lower semantic match."
}
```
[3] Mapping Legacy attribute: ACCT_CUST_ORG_COD
RAW LLM OUTPUT:
RAW LLM OUTPUT:
 ```json
 ```json
{
  "primary_match": "ACCOUNT_ACCOUNTIDENTIFICATION_NUMBER",
  "alternates": ["ACCOUNT_CARDPROGRAM_ORGANISATIONID_BICFI"],
  "confidence": "Medium",
  "reasoning": "ACCT_CUST_ORG_COD represents a customer organization code, which aligns best with ACCOUNT_ACCOUNTIDENTIFICATION_NUMBER as a general account identifier, despite the datatype difference. ACCOUNT_CARDPROGRAM_ORGANISATIONID_BICFI is less relevant due to its specific context."  
  "confidence": "Medium",
  "reasoning": "ACCT_CUST_ORG_COD represents a customer organization code, which aligns best with ACCOUNT_ACCOUNTIDENTIFICATION_NUMBER as a general account identifier, despite the datatype difference. ACCOUNT_CARDPROGRAM_ORGANISATIONID_BICFI is less relevant due to its specific context."  
  "reasoning": "ACCT_CUST_ORG_COD represents a customer organization code, which aligns best with ACCOUNT_ACCOUNTIDENTIFICATION_NUMBER as a general account identifier, despite the datatype difference. ACCOUNT_CARDPROGRAM_ORGANISATIONID_BICFI is less relevant due to its specific context."  
al account identifier, despite the datatype difference. ACCOUNT_CARDPROGRAM_ORGANISATIONID_BICFI is less relevant due to its specific context."  
}
```

Writing final output Excel...
Results written to: data\output\Probable_Mapping_Results.xlsx

Mapping completed successfully!
 Output file: data/output/Probable_Mapping_Results.xlsx

(venv) C:\Users\arist\genai_training\vscodestuff\MAP_POC\rag-data-mapping-poc>