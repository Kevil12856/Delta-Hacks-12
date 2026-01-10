import os
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_voyageai import VoyageAIEmbeddings
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
    print("Using Voyage AI Embeddings (Legal Optimized) - Full Speed Results 🚀")
    return VoyageAIEmbeddings(model="voyage-law-2") 

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
        # List of files to ingest
        target_files = ["docs/bc_rta_full.html", "docs/alberta_rta_full.html"]
        
        for file in target_files:
            if os.path.exists(file):
                 ingest_data(file)
            else:
                 print(f"Warning: {file} not found.")
