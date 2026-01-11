import os
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
from langchain_voyageai import VoyageAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# Official Sources
# --- Configuration ---
# Using CanLII or stable government endpoints where possible.
# Adding User-Agent to mimic browser.

# --- Configuration ---
# Adding Criminal, Tax, and Business Laws (Federal).
# Prioritizing laws-lois.justice.gc.ca as it allows scraping with headers.

LAW_SOURCES = [
    {
        "name": "Criminal Code (Federal)",
        "url": "https://laws-lois.justice.gc.ca/eng/acts/C-46/FullText.html",
        "category": "CRIMINAL",
        "jurisdiction": "FEDERAL"
    },
    {
        "name": "Income Tax Act (Federal)",
        "url": "https://laws-lois.justice.gc.ca/eng/acts/I-3.3/FullText.html",
        "category": "TAX",
        "jurisdiction": "FEDERAL"
    },
    {
        "name": "Canada Business Corporations Act (Federal)",
        "url": "https://laws-lois.justice.gc.ca/eng/acts/C-44/FullText.html",
        "category": "BUSINESS",
        "jurisdiction": "FEDERAL"
    },
    {
        "name": "Excise Tax Act (GST/HST)",
        "url": "https://laws-lois.justice.gc.ca/eng/acts/E-15/FullText.html",
        "category": "TAX",
        "jurisdiction": "FEDERAL"
    },
    {
        "name": "Immigration and Refugee Protection Act (Federal)",
        "url": "https://laws-lois.justice.gc.ca/eng/acts/I-2.5/FullText.html", 
        "category": "IMMIGRATION",
        "jurisdiction": "FEDERAL"
    }
]

def get_db_connection():
    try:
        client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())
        return client["juris_db"]["legal_docs"]
    except Exception as e:
        print(f"DB Connection Error: {e}")
        return None

def fetch_and_parse(url):
    print(f"Fetching {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        
        # Cleanup: Remove scripts, styles
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()
            
        content = soup.get_text(separator="\n")
        
        # Validation: If content is too short, it likely failed.
        if len(content) < 1000:
            print(f"WARNING: Content too short ({len(content)} chars). Might be a captcha or blocking page.")
            return None
            
        return content
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def main():
    collection = get_db_connection()
    if collection is None:
        return

    embeddings = VoyageAIEmbeddings(model="voyage-law-2")
    vector_store = MongoDBAtlasVectorSearch(
        collection=collection,
        embedding=embeddings,
        index_name="vector_index"
    )
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    for source in LAW_SOURCES:
        print(f"\n--- Processing: {source['name']} ---")
        text = fetch_and_parse(source['url'])
        if not text:
            continue
            
        print(f"Extracted {len(text)} characters. Splitting...")
        chunks = splitter.create_documents(
            [text], 
            metadatas=[{
                "source": source['name'],
                "url": source['url'],
                "category": source['category'],
                "jurisdiction": source['jurisdiction']
            }]
        )
        print(f"Created {len(chunks)} chunks. Ingesting to MongoDB...")
        
        # Ingest in batches to avoid timeouts
        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            vector_store.add_documents(batch)
            print(f"Upserted batch {i} - {i+len(batch)}")
            
    print("\n✅ Ingestion Complete!")

if __name__ == "__main__":
    main()
