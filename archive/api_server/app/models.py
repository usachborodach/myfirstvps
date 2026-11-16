from pydantic import BaseModel
from typing import Any, Dict, Optional

class ResponseMessage(BaseModel):
    message: str
    detail: Optional[Any] = None