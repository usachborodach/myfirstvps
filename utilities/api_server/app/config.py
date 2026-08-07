import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    TOKEN: str = os.getenv("TOKEN", "default-secret-token")
    BASE_API_URL: str = os.getenv("BASE_API_URL", "default-secret-token")

settings = Settings()