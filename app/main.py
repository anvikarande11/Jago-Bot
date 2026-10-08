from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# 1. CREATE THE FASTAPI APP INSTANCE FIRST
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API engine for the Unified MoTA Scholarship Portal and JAGO Chatbot.",
    version=settings.VERSION,
    lifespan=lifespan
)

# 2. Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include Routers
app.include_router(chat.router)

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs_url": "/docs"
    }

# 4. MOUNT STATIC FILES LAST (so app is fully defined)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")