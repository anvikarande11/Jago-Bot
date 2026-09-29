import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "JAGO MoTA Chatbot API"
    VERSION: str = "1.0.0"
    # Make the OpenAI key optional so it doesn't break if you aren't using it
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "not-needed-for-ollama")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./mota.db")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()