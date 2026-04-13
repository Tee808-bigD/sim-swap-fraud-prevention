from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.transaction import Transaction, TransactionStatus
from ..schemas.transaction import TransactionCreate, TransactionResponse
from ..services.fraud_detector import fraud_detector
from ..services.ai_engine import ai_engine
from ..models.fraud_alert import FraudAlert, AlertType, RiskLevel, ActionTaken

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # Create transaction record
    db_transaction = Transaction(
        phone_number=transaction.phone_number,
        amount=transaction.amount,
        currency=transaction.currency,
        transaction_type=transaction.transaction_type,
        recipient=transaction.recipient,
        status=TransactionStatus.PENDING
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Run fraud detection
    risk_analysis = await fraud_detector.compute_risk_score(transaction.dict())
    ai_decision = await ai_engine.analyze_fraud_risk(transaction.dict(), risk_analysis)
    
    # Update transaction status
    if ai_decision["decision"] == "BLOCK":
        db_transaction.status = TransactionStatus.BLOCKED
    elif ai_decision["decision"] == "APPROVE":
        db_transaction.status = TransactionStatus.APPROVED
    else:
        db_transaction.status = TransactionStatus.FLAGGED
    
    db_transaction.risk_score = risk_analysis["risk_score"]
    db.commit()
    
    # Create fraud alert if needed
    if ai_decision["decision"] != "APPROVE":
        alert = FraudAlert(
            transaction_id=db_transaction.id,
            phone_number=transaction.phone_number,
            alert_type=AlertType.COMPOSITE,
            risk_level=RiskLevel(risk_analysis["risk_level"]),
            camara_checks={"sim_swap": risk_analysis.get("sim_swap_detected"), 
                          "device_swap": risk_analysis.get("device_swap_detected")},
            ai_analysis=ai_decision,
            action_taken=ActionTaken(ai_decision["decision"].lower())
        )
        db.add(alert)
        db.commit()
    
    return db_transaction

@router.get("/", response_model=List[TransactionResponse])
def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Transaction).offset(skip).limit(limit).all()