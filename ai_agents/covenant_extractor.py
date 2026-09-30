import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# root synapsis folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# forcing to find the .env file and override any terminal cache
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH, override=True)

DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# JSON schema for the LLM to follow
class CovenantRules(BaseModel):
    max_leverage_ratio: float = Field(description="The maximum allowed leverage ratio (e.g., 3.5)")
    min_interest_coverage: float = Field(description="The minimum allowed interest coverage ratio (e.g., 2.5)")
    breach_penalties: list[str] = Field(description="List of penalties or consequences if covenants are breached")

def extract_covenants_from_db(collection_name: str = "covenants") -> CovenantRules:
    print(f"🔍 Connecting to ChromaDB at: {DB_PATH}")
    
    # connecting to the existing vector database created in Test 1
    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=OpenAIEmbeddings(),
        collection_name=collection_name
    )
    
    # searching the database for the exact paragraphs discussing financial constraints
    print("🔎 Searching database for covenant clauses...")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    query = "What are the financial covenants, specifically maximum leverage ratio, minimum interest coverage ratio, and breach penalties?"
    docs = retriever.invoke(query)
    
    # stitching the retrieved paragraphs together
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    print("🧠 Sending legal context to GPT-4o-mini for structured extraction...")
    
    # setting the LLM (temperature=0 ensures it doesn't hallucinate numbers)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(CovenantRules)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert financial risk analyst. Extract the exact covenant limits and penalties from the provided SEC legal text. If a value is not explicitly stated, guess based on context or return 0.0 if entirely absent."),
        ("human", "Here is the SEC document context:\n\n{context}")
    ])
    
    # chaining the prompt and the LLM together
    chain = prompt | structured_llm
    rules = chain.invoke({"context": context_text})
    
    print("✅ Extraction complete!")
    return rules

if __name__ == "__main__":
    rules = extract_covenants_from_db()
    print("\n--- Extracted Rules ---")
    print(rules.model_dump_json(indent=2))