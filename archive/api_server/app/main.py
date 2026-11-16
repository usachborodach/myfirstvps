from fastapi import FastAPI
from app.routes.mongo import router as mongo_router

app = FastAPI(title="MongoDB Service")
app.include_router(mongo_router, prefix="/mongo", tags=["mongo"])