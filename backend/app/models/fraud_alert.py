import enum
from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base

class AlertType(str, enum.Enum):
    SIM_SWAP = "sim_swap"
    DEVICE_SWAP = "device_swap"
    NUMBER_MISMATCH = "number_mismatch"
    COMPOSITE = "composite"

class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ActionTaken(str, enum.Enum):
    BLOCKED = "blocked"
    APPROVED = "approved"
    FLAGGED = "flagged"

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id"), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    alert_type: Mapped[AlertType] = mapped_column(Enum(AlertType))
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel))
    camara_checks: Mapped[dict] = mapped_column(JSON, default=dict)
    ai_analysis: Mapped[dict] = mapped_column(JSON, default=dict)
    action_taken: Mapped[ActionTaken] = mapped_column(Enum(ActionTaken))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))