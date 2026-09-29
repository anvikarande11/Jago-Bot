from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import chat
import app.models.mota_models  # Ensure models are registered

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ SQLite Database tables created successfully!")
    yield

# Single, unified FastAPI app instance with all configurations and lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API engine for the Unified MoTA Scholarship Portal and JAGO Chatbot.",
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs_url": "/docs"
    }