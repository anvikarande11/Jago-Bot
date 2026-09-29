from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PERSIST_DIR = "./chroma_db"

def test_search():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Load the persisted Chroma database
    vector_store = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="mota_scheme_guidelines"
    )
    
    # Test query about a MoTA scheme
    query = "What are the eligibility criteria for the Post-Matric scholarship?"
    print(f"🔍 Searching database for: '{query}'\n")
    
    results = vector_store.similarity_search(query, k=3)
    
    for i, doc in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(doc.page_content[:300] + "...\n")

if __name__ == "__main__":
    test_search()