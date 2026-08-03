from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

_client: AsyncIOMotorClient = None

async def connect_to_mongo():
    global _client
    _client = AsyncIOMotorClient(MONGO_URI)
    await _client.admin.command('ping')

async def close_mongo_connection():
    global _client
    if _client:
        _client.close()

def get_collection():
    if _client is None:
        raise RuntimeError("MongoDB not connected")
    return _client[DB_NAME][COLLECTION_NAME]