from langchain_voyageai import VoyageAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def check_dims():
    try:
        embeddings = VoyageAIEmbeddings(model="voyage-law-2")
        vector = embeddings.embed_query("test")
        print(f"✅ Voyage-law-2 Dimension: {len(vector)}")
        
        # Also check standard voyage-2 just in case
        embeddings_std = VoyageAIEmbeddings(model="voyage-2")
        vector_std = embeddings_std.embed_query("test")
        print(f"✅ Voyage-2 Dimension: {len(vector_std)}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_dims()
