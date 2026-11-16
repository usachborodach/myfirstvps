from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

def get_collection(db_name: str, collection_name: str):
    return client[db_name][collection_name]