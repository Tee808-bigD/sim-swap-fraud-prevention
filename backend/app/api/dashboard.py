from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database import get_db
from ..models.transaction import Transaction, TransactionStatus
from ..models.fraud_alert import FraudAlert

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_transactions = db.query(Transaction).count()
    blocked = db.query(Transaction).filter(Transaction.status == TransactionStatus.BLOCKED).count()
    approved = db.query(Transaction).filter(Transaction.status == TransactionStatus.APPROVED).count()
    flagged = db.query(Transaction).filter(Transaction.status == TransactionStatus.FLAGGED).count()
    
    fraud_alerts = db.query(FraudAlert).count()
    
    return {
        "total_transactions": total_transactions,
        "blocked": blocked,
        "approved": approved,
        "flagged": flagged,
        "approval_rate": round((approved / total_transactions * 100) if total_transactions > 0 else 0, 1),
        "fraud_alerts": fraud_alerts,
        "total_amount_saved": blocked * 500
    }

@router.get("/timeline")
def get_timeline(days: int = 7, db: Session = Depends(get_db)):
    date_threshold = datetime.now() - timedelta(days=days)
    transactions = db.query(Transaction).filter(Transaction.created_at >= date_threshold).all()
    
    timeline = {}
    for tx in transactions:
        date = tx.created_at.strftime("%Y-%m-%d")
        if date not in timeline:
            timeline[date] = {"total": 0, "blocked": 0, "approved": 0}
        timeline[date]["total"] += 1
        if tx.status == TransactionStatus.BLOCKED:
            timeline[date]["blocked"] += 1
        elif tx.status == TransactionStatus.APPROVED:
            timeline[date]["approved"] += 1
    
    return [{"date": d, **v} for d, v in timeline.items()]