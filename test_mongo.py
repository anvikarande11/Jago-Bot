import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    try:
        MONGO_URI = os.getenv("MONGO_URI")
        client = AsyncIOMotorClient(MONGO_URI)
        # Ping the server to check connectivity
        await client.admin.command('ping')
        print("✅ SUCCESS: Connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ ERROR: Could not connect to MongoDB: {e}")

asyncio.run(test_connection())