from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.fraud_alert import FraudAlert
from ..schemas.fraud_alert import FraudAlertResponse

router = APIRouter()

@router.get("/alerts", response_model=List[FraudAlertResponse])
def get_fraud_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(FraudAlert).order_by(FraudAlert.created_at.desc()).offset(skip).limit(limit).all()