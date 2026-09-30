# Synapse Engine: Automated RAG for Regulatory Operations

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://synapsis.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-green)](https://www.langchain.com/)

**Synapse Engine** is an Agentic RAG (Retrieval-Augmented Generation) pipeline designed to automate the extraction of financial covenants from complex, unstructured SEC filings. 

Built specifically for Middle Office, Risk, and Regulatory Reporting workflows, this tool eliminates manual data entry, accelerates reporting timelines, and enforces strict audit-readiness by structuring legal text into rigid JSON formats.

## Business Value
In traditional compliance operations, manually extracting constraints like *Maximum Leverage Ratios* from 100-page credit agreements creates operational bottlenecks and increases the risk of human error. 

The Synapse Engine solves this by:
*   **Reducing Operational Risk:** Replaces manual "fat-finger" data entry with deterministic AI extraction.
*   **Enforcing Control Frameworks:** Utilizes strict Pydantic schemas to ensure data is correctly typed and ready for downstream SQL databases or regulatory reports (Form PF, N-Port).
*   **Maintaining Audit Trails:** Employs local Vector Databases (Chroma) to ensure every extracted metric can be traced back to the exact chunk of the original legal text.

## System Architecture

The pipeline is broken into three core phases:

1.  **Secure Document Ingestion (`document_vectorizer.py`)**
    *   Ingests PDF SEC filings (e.g., Exhibit 10.1 Credit Agreements) via `PyPDFLoader`.
    *   Applies a `RecursiveCharacterTextSplitter` (2000-character chunks with 200-character overlap) to preserve legal context without cutting clauses in half.
    *   Generates mathematical embeddings via `OpenAIEmbeddings` and stores them locally in `ChromaDB`.

2.  **Structured AI Extraction (`covenant_extractor.py`)**
    *   Queries the vector database for clauses pertaining to financial constraints and breach penalties.
    *   Passes the retrieved context to `GPT-4o-mini` (temperature = 0) with a strict instruction to act as a Risk Analyst.
    *   Uses `Pydantic` to force the LLM output into a rigid JSON structure, eliminating hallucinated formatting.

3.  **Live Risk Dashboard (`app.py`)**
    *   A frontend `Streamlit` application that simulates a live compliance monitor.
    *   Compares the extracted covenants against simulated live market data (e.g., current debt ratios) to instantly flag threshold breaches for Risk Committee escalation.

## Tech Stack
*   **Backend / Logic:** Python 3, LangChain, Pydantic
*   **AI / Embeddings:** OpenAI API (`gpt-4o-mini`, `text-embedding-3-small`)
*   **Database:** ChromaDB (Local Vector Store)
*   **Frontend:** Streamlit Community Cloud

## Run it Locally

To test the Synapse Engine on your local machine:

**1. Clone the repository:**
```bash
git clone https://github.com/GravityD9/Synapsis.git
cd Synapsis
