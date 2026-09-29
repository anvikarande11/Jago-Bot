import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_chroma import Chroma

CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "mota_scheme_guidelines"

class RAGService:
    def __init__(self):
        # Initialize local Ollama models
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.llm = Ollama(model="llama3", temperature=0.1)
        
        # Load vector store safely
        try:
            self.vector_store = Chroma(
                persist_directory=CHROMA_PERSIST_DIR,
                embedding_function=self.embeddings,
                collection_name=COLLECTION_NAME
            )
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize Chroma vector store: {e}")
            self.vector_store = None

    def query_rag(self, user_message: str):
        if not self.vector_store:
            # Fallback if DB isn't loaded
            response = self.llm.invoke(f"You are Jago Bot, an official AI assistant for the MoTA Scholarship Portal. Answer directly:\n\n{user_message}")
            return {"reply": response, "sources_found": 0}

        # 1. Fast similarity search (k=2 for low latency)
        docs = self.vector_store.similarity_search(user_message, k=2)
        context = "\n\n".join([doc.page_content for doc in docs]) if docs else ""

        # 2. Hybrid prompt design (uses context if found, allows general fallback smoothly)
        if context.strip():
            prompt = f"""You are Jago Bot, an official AI assistant for the MoTA Scholarship Portal. Answer the user's question accurately using the official guidelines context below.

Context:
{context}

User Question: {user_message}
Answer:"""
        else:
            prompt = f"""You are Jago Bot, an official AI assistant for the MoTA Scholarship Portal. Answer the user's question directly and concisely.

User Question: {user_message}
Answer:"""

        # 3. Fast generation
        response = self.llm.invoke(prompt)
        
        return {
            "reply": response,
            "sources_found": len(docs)
        }

# Singleton instance to import into your chat router
rag_service = RAGService()