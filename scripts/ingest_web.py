import os
import urllib3
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

# Suppress SSL warning output in the terminal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "mota_scheme_guidelines"

def ingest_official_website():
    target_urls = [
        "https://tribal.nic.in/",
        "https://tribal.nic.in/home.aspx",
        "https://tribal.nic.in/Finance.aspx",
        "https://dbttribal.gov.in/"
    ]

    print("🌐 Scraping content from official Ministry of Tribal Affairs web pages...")
    
    # Pass requests_kwargs={'verify': False} to bypass local SSL verification errors
    loader = WebBaseLoader(target_urls, requests_kwargs={'verify': False})
    docs = loader.load()
    print(f"✅ Successfully loaded {len(docs)} web documents.")

    print("✂️ Splitting web documents into clean text chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(docs)
    print(f"✅ Generated {len(chunks)} chunks from the website.")

    print("🧠 Initializing Ollama embeddings (nomic-embed-text)...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print(f"📦 Storing web chunks into local Chroma database at '{CHROMA_PERSIST_DIR}'...")
    
    vector_store = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )
    
    vector_store.add_documents(chunks)
    print(f"🎉 Success! Added official website data into Chroma database.")

if __name__ == "__main__":
    ingest_official_website()