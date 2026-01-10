import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_voyageai import VoyageAIEmbeddings
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "juris_db"
COLLECTION_NAME = "legal_docs"
INDEX_NAME = "vector_index"
MONGODB_URI = os.getenv("MONGODB_URI")

def test_retrieval():
    print("--- 🔍 Debugging Vector Store ---")
    
    # 1. Connect to Mongo directly to count docs
    try:
        client = MongoClient(MONGODB_URI)
        collection = client[DB_NAME][COLLECTION_NAME]
        total_count = collection.count_documents({})
        ab_count = collection.count_documents({"jurisdiction": "AB"})
        bc_count = collection.count_documents({"jurisdiction": "BC"})
        on_count = collection.count_documents({"jurisdiction": "ON"})
        
        print(f"📉 Total Documents in DB: {total_count}")
        print(f"   - ON Docs: {on_count}")
        print(f"   - BC Docs: {bc_count}")
        print(f"   - AB Docs: {ab_count}")
        
        if ab_count == 0:
            print("❌ CRITICAL: No Alberta documents found in raw Mongo collection!")
    except Exception as e:
        print(f"❌ Mongo Connection Error: {e}")
        return

    # 2. Test Vector Search through LangChain
    embeddings = VoyageAIEmbeddings(model="voyage-law-2")
    vector_store = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string=MONGODB_URI,
        namespace=f"{DB_NAME}.{COLLECTION_NAME}",
        embedding=embeddings,
        index_name=INDEX_NAME
    )
    
    queries = [
        ("AB", "mold in basement"),
        ("BC", "rent increase"),
        ("ON", "eviction for personal use")
    ]
    
    print("\n--- 🧪 Filtered Search Test ---")
    queries = [
        ("AB", "mold in basement"),
        ("BC", "rent increase")
    ]

    for jur, query in queries:
        print(f"\nQUERY: '{query}' (Filter: {jur})")
        results = vector_store.similarity_search(
            query,
            k=3,
            pre_filter={"jurisdiction": jur} # Now using correct pre_filter key?
            # Actually, let's try the key that worked in my head: "jurisdiction" matches schema
        )
        for doc in results:
             print(f"   ✅ Found: {doc.metadata.get('source')}")
             print(f"      Preview: {doc.page_content[:100]}...")

if __name__ == "__main__":
    test_retrieval()
