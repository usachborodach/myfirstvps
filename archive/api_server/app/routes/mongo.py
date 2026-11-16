from fastapi import APIRouter, HTTPException, Depends, Body
from bson import ObjectId
from typing import List, Dict, Any
from app.database import get_collection
from app.dependencies import verify_token
from app.models import ResponseMessage

router = APIRouter()

def serialize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/{db}/{collection}", response_model=Dict[str, Any])
async def create_document(
    db: str,
    collection: str,
    document: Dict[str, Any] = Body(...),
    token: str = Depends(verify_token)
):
    coll = get_collection(db, collection)
    result = await coll.insert_one(document)
    if result.inserted_id:
        new_doc = await coll.find_one({"_id": result.inserted_id})
        return serialize_document(new_doc)
    raise HTTPException(status_code=500, detail="Failed to insert document")

@router.get("/{db}/{collection}", response_model=List[Dict[str, Any]])
async def get_all_documents(
    db: str,
    collection: str,
    token: str = Depends(verify_token)
):
    coll = get_collection(db, collection)
    cursor = coll.find({})
    documents = []
    async for doc in cursor:
        documents.append(serialize_document(doc))
    return documents

@router.delete("/{db}/{collection}/{id}", response_model=ResponseMessage)
async def delete_document(
    db: str,
    collection: str,
    id: str,
    token: str = Depends(verify_token)
):
    coll = get_collection(db, collection)
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    result = await coll.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return ResponseMessage(message="Document deleted successfully")

@router.put("/{db}/{collection}/{id}", response_model=Dict[str, Any])
async def update_document(
    db: str,
    collection: str,
    id: str,
    document: Dict[str, Any] = Body(...),
    token: str = Depends(verify_token)
):
    coll = get_collection(db, collection)
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    document.pop("_id", None)  # защита от попытки обновить _id
    result = await coll.replace_one({"_id": object_id}, document)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    updated = await coll.find_one({"_id": object_id})
    return serialize_document(updated)