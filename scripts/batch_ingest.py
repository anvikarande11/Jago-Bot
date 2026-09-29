import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

PDF_PATH = "./data/mota_pdfs/mota_.pdf"
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "mota_scheme_guidelines"

def run_ingestion():
    if not os.path.exists(PDF_PATH):
        print(f"❌ Error: PDF file not found at {PDF_PATH}")
        return

    print("📄 Loading PDF document...")
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()
    print(f"✅ Loaded {len(pages)} pages successfully.")

    print("✂️ Splitting document into text chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(pages)
    print(f"✅ Generated {len(chunks)} text chunks.")

    print("🧠 Initializing Ollama embeddings (nomic-embed-text)...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print(f"📦 Storing chunks into local Chroma database at '{CHROMA_PERSIST_DIR}'...")
    
    # Direct, single-pass storage just like the original setup
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
        collection_name=COLLECTION_NAME
    )

    print(f"🎉 Success! All {len(chunks)} chunks stored securely in Chroma.")

if __name__ == "__main__":
    run_ingestion()