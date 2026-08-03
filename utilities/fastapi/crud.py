from bson import ObjectId
from fastapi import HTTPException
from models import QuoteOut, QuoteUpdate
from database import get_collection

async def get_quote_document(quote_id: str):
    """Возвращает документ по ID или выбрасывает 404."""
    try:
        obj_id = ObjectId(quote_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    collection = get_collection()
    doc = await collection.find_one({"_id": obj_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Quote not found")
    return doc

async def create_quote(quote_data):
    collection = get_collection()
    result = await collection.insert_one(quote_data.dict())
    inserted = await collection.find_one({"_id": result.inserted_id})
    return QuoteOut(**inserted)

async def get_quotes(skip: int, limit: int, category: str = None):
    collection = get_collection()
    filter_criteria = {}
    if category:
        filter_criteria["category"] = category
    cursor = collection.find(filter_criteria).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    return [QuoteOut(**doc) for doc in docs]

async def update_quote(quote_id: str, update_data: QuoteUpdate):
    collection = get_collection()
    # Проверяем существование
    await get_quote_document(quote_id)
    # Формируем словарь только с переданными полями
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")
    await collection.update_one(
        {"_id": ObjectId(quote_id)},
        {"$set": update_dict}
    )
    updated = await collection.find_one({"_id": ObjectId(quote_id)})
    return QuoteOut(**updated)

async def delete_quote(quote_id: str):
    collection = get_collection()
    await get_quote_document(quote_id)  # проверяем, что существует
    await collection.delete_one({"_id": ObjectId(quote_id)})