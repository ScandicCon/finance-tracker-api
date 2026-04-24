from pydantic import BaseModel
from typing import Optional
class CategoryCreate(BaseModel):
    name: int

class CategoryResponce(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True



class CategoryUpdate(BaseModel):
    name: Optional[str] = None