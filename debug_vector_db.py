import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch

load_dotenv()

def debug_db():
    print("--- DEBUGGING VECTOR DB ---")
    
    # 1. Connect
    try:
        client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())
        db = client["juris_db"]
        col = db["legal_docs"]
        print(f"Connected to DB. Collection: {col.name}")
    except Exception as e:
        print(f"Connection Failed: {e}")
        return

    # 2. Count
    count = col.count_documents({})
    print(f"Total Documents in Collection: {count}")
    
    if count == 0:
        print("CRITICAL: Collection is EMPTY! You need to run ingest.py again.")
        return

    # 3. Check Metadata Sample
    sample = col.find_one()
    print("\n--- SAMPLE DOCUMENT METADATA ---")
    print(sample.get('metadata', "No metadata found"))
    
    # 4. Test Search with "ON" Filter
    print("\n--- TEST SEARCH (Filter: jurisdiction='ON') ---")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    vstore = MongoDBAtlasVectorSearch(
        collection=col,
        embedding=embeddings,
        index_name="vector_index"
    )
    
    query = "divorce adultery requirements"
    try:
        results = vstore.similarity_search(query, k=2, pre_filter={"jurisdiction": {"$in": ["ON", "FEDERAL"]}})
        print(f"Query: '{query}'")
        print(f"Found {len(results)} results.")
        for i, res in enumerate(results):
            print(f"Result {i+1}: {res.metadata.get('source')} (Score: N/A)")
    except Exception as e:
        print(f"Search Failed: {e}")

if __name__ == "__main__":
    debug_db()
