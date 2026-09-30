import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# root folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# to find the .env file and override any terminal cache
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH, override=True)

DB_PATH = os.path.join(BASE_DIR, "chroma_db")

def vectorize_pdf(pdf_path: str, collection_name: str = "covenants"):
    # ensuring the PDF path maps perfectly to the root directory
    absolute_pdf_path = os.path.join(BASE_DIR, pdf_path) if not os.path.isabs(pdf_path) else pdf_path
    
    print(f"📄 Loading SEC document: {absolute_pdf_path}")
    loader = PyPDFLoader(absolute_pdf_path)
    docs = loader.load()
    
    print("✂️ Chunking text to preserve legal context...")
    # 2000 characters with a 200 character overlap prevents cutting a legal clause in half
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, 
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(docs)
    
    print(f"🧠 Embedding and saving to ChromaDB at: {DB_PATH} ...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=DB_PATH,
        collection_name=collection_name
    )
    
    print(f"✅ Successfully embedded {len(chunks)} chunks into the local Vector DB!")
    return vectorstore

if __name__ == "__main__":
    # pass the relative path from the root folder
    vectorize_pdf("data/credit_agreements/credit_agreement.pdf")