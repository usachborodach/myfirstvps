from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class QuoteIn(BaseModel):
    text: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)

class QuoteUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1)

class QuoteOut(BaseModel):
    id: str = Field(..., alias="_id")
    text: str
    category: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}