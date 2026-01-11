import os
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Configuration
DB_NAME = "juris_db"
COLLECTION_NAME = "legal_docs"
INDEX_NAME = "vector_index"
MONGODB_URI = os.getenv("MONGODB_URI")


JURISDICTION_MAP = {
    "ontario_rta.html": "ON",
    "bc_rta_full.html": "BC",
    "alberta_rta_full.html": "AB"
}

def get_embeddings():
    print("Using Google Gemini Embeddings (text-embedding-004) 🧠")
    return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def ingest_data(file_path):
    print(f"--- Starting Ingestion for {file_path} ---")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Load
    if file_path.endswith(".html"):
        loader = BSHTMLLoader(file_path)
    else:
        loader = PyPDFLoader(file_path)
    
    docs = loader.load()
    
    # Metadata Tagging
    filename = os.path.basename(file_path)
    jurisdiction = JURISDICTION_MAP.get(filename, "General")
    
    for doc in docs:
        doc.metadata["jurisdiction"] = jurisdiction
        doc.metadata["source"] = filename
    
    # Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    print(f"Docs split into {len(splits)} chunks. Jurisdiction: {jurisdiction}")

    # Embed & Store
    embeddings = get_embeddings()
    collection = MongoClient(MONGODB_URI)[DB_NAME][COLLECTION_NAME]
    
    print(f"Pushing to MongoDB Atlas [{DB_NAME}.{COLLECTION_NAME}]...")
    
    # Efficiently ingest all documents
    MongoDBAtlasVectorSearch.from_documents(
        documents=splits,
        embedding=embeddings,
        collection=collection,
        index_name=INDEX_NAME
    )
    
    print("✅ Ingestion Complete! Data is now in Atlas.")

if __name__ == "__main__":
    if not MONGODB_URI:
        print("CRITICAL: MONGODB_URI is missing in .env")
    else:
        # Wipe existing data to prevent dimension mismatch
        print("⚠ Wiping existing collection to prevent vector dimension mismatch...")
        MongoClient(MONGODB_URI)[DB_NAME][COLLECTION_NAME].delete_many({})
        print("Collection cleared.")

        # List of files to ingest
        target_files = ["docs/ontario_rta.html", "docs/bc_rta_full.html", "docs/alberta_rta_full.html"]
        
        for file in target_files:
            if os.path.exists(file):
                 ingest_data(file)
            else:
                 print(f"Warning: {file} not found.")
