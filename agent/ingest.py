import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_mongodb import MongoDBAtlasVectorSearch
# from langchain_voyageai import VoyageAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def ingest_data(file_path):
    print(f"Ingesting {file_path}...")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    
    print(f"Split into {len(splits)} chunks.")
    
    # TODO: Initialize Vector Store and add documents
    # embeddings = VoyageAIEmbeddings(model="voyage-law-2")
    # vector_store = MongoDBAtlasVectorSearch.from_documents(
    #     documents=splits,
    #     embedding=embeddings,
    #     collection=...
    # )
    print("Ingestion complete (Placeholder).")

if __name__ == "__main__":
    # Example usage
    ingest_data("docs/residential_tenancies_act.pdf")
