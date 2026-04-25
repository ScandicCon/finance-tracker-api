from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date as date_type
from decimal import Decimal

from app.utils.enums import TransactionType


class TransactionCreate(BaseModel):
    amount: Decimal
    type: TransactionType
    category_id: int
    description: Optional[str] = None
    date: date_type


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    type: TransactionType
    description: Optional[str]
    date: date_type
    created_at: datetime
    user_id: int
    category_id: int

    class Config:
        from_attributes = True

class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = None
    type: Optional[TransactionType] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    date: Optional[date_type] = None