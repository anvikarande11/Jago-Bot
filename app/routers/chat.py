from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_chroma import Chroma
from dotenv import load_dotenv  # <--- Make sure this is imported
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

router = APIRouter(prefix="/api", tags=["Chat"])

CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "mota_scheme_guidelines"

# Initialize MongoDB Client & Collection asynchronously
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client.jago_chatbot
chat_collection = db.conversations

# Initialize standard local Ollama embeddings and LLM
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = Ollama(model="llama3", temperature=0.1)

# Load the local Chroma vector store safely on startup
try:
    vector_store = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )
except Exception as e:
    print(f"⚠️ Warning: Could not load Chroma vector store: {e}")
    vector_store = None

class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "English"  # Defaults strictly to English unless stated otherwise
    session_id: Optional[str] = "default_user"

@router.post("/chat")
async def chat_with_jago(request: ChatRequest):
    try:
        docs = []
        context = ""
        
        # 1. Similarity search
        if vector_store:
            docs = vector_store.similarity_search(request.message, k=2)
            context = "\n\n".join([doc.page_content for doc in docs]) if docs else ""

        # 2. General query detection
        query_lower = request.message.lower()
        is_general_query = any(term in query_lower for term in ["president", "prime minister", "capital", "who is", "what is the capital", "weather", "india's"])

        # 3. Dynamic language directive based on user request
        requested_lang = request.language.strip() if request.language else "English"
        if requested_lang.lower() == "english":
            lang_instruction = "\nInstruction: Respond clearly and professionally in English."
        else:
            lang_instruction = f"\nInstruction: You must translate and respond entirely in {requested_lang}."

        if is_general_query:
            prompt = f"""You are Jago Bot, an official AI assistant for the Ministry of Tribal Affairs. Answer the user's general knowledge question directly, accurately, and articulately.{lang_instruction}

User Question: {request.message}
Answer:"""
        elif context.strip():
            prompt = f"""You are Jago Bot, an official AI assistant for the Ministry of Tribal Affairs (MoTA) Scholarship Portal. Answer the user's question thoroughly and accurately using the official guidelines context below.{lang_instruction}

Context:
{context}

User Question: {request.message}
Answer:"""
        else:
            prompt = f"""You are Jago Bot, an official AI assistant for the Ministry of Tribal Affairs (MoTA) Scholarship Portal. Answer the user's question directly and concisely.{lang_instruction}

User Question: {request.message}
Answer:"""

        # 4. Generate response
        response = llm.invoke(prompt)
        timestamp_str = datetime.utcnow().isoformat()

        # 5. Save conversation record to MongoDB asynchronously
        chat_record = {
            "session_id": request.session_id,
            "user_message": request.message,
            "bot_reply": response,
            "language_used": requested_lang,
            "sources_found": len(docs),
            "timestamp": timestamp_str
        }
        await chat_collection.insert_one(chat_record)
        
        return {
            "status": "success",
            "query": request.message,
            "language_used": requested_lang,
            "reply": response,
            "sources_found": len(docs)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))