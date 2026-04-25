from pydantic import BaseModel
from typing import Optional
from app.utils.enums import TransactionType

class CategoryCreate(BaseModel):
    name: str
    type: TransactionType

class CategoryResponse(BaseModel):
    id: int
    name: str
    type: TransactionType
    class Config:
        from_attributes = True



class CategoryUpdate(BaseModel):
    name: Optional[str] = None