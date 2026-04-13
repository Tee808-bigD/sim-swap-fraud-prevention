from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class SimCheck(Base):
    __tablename__ = "sim_checks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    sim_swap_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    swap_date: Mapped[str] = mapped_column(String(50), nullable=True)
    device_swap_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    device_swap_date: Mapped[str] = mapped_column(String(50), nullable=True)
    number_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    check_results: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))