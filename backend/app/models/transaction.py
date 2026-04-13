import enum
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, DateTime, Enum, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base

class TransactionType(str, enum.Enum):
    SEND = "send"
    RECEIVE = "receive"

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    BLOCKED = "blocked"
    FLAGGED = "flagged"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="KES")
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    recipient: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    risk_score: Mapped[int] = mapped_column(Integer, default=0)
    fraud_alert_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))