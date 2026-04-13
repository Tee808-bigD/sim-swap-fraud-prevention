from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from ..models.transaction import TransactionType, TransactionStatus

class TransactionCreate(BaseModel):
    phone_number: str
    amount: float
    currency: str = "KES"
    transaction_type: TransactionType
    recipient: Optional[str] = None
    is_new_recipient: bool = False

class TransactionResponse(BaseModel):
    id: int
    phone_number: str
    amount: float
    currency: str
    transaction_type: TransactionType
    recipient: Optional[str]
    status: TransactionStatus
    risk_score: int
    created_at: datetime
    
    class Config:
        from_attributes = True