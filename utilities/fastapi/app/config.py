import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    STATIC_TOKEN: str = os.getenv("STATIC_TOKEN", "default-secret-token")

settings = Settings()