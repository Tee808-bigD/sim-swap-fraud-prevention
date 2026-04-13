from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI(title="SimGuard API", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TransactionCheck(BaseModel):
    phone_number: str
    amount: float
    currency: str = "KES"
    recipient: Optional[str] = None
    is_new_recipient: bool = False

class TransactionResponse(BaseModel):
    id: str
    phone_number: str
    amount: float
    currency: str
    status: str
    risk_score: int
    message: str

# SIM swap detection logic
def detect_sim_swap(phone_number: str):
    # Test numbers from Nokia
    if phone_number == "+99999991000":
        return True, "SIM swap detected 2 hours ago"
    elif phone_number == "+99999991001":
        return False, "No SIM swap detected"
    # Random detection for demo
    return False, "No issues detected"

# API Endpoints
@app.get("/")
async def root():
    return {"message": "SimGuard API is running", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/transactions")
async def check_transaction(transaction: TransactionCheck):
    # Run SIM swap detection
    sim_swap_detected, sim_message = detect_sim_swap(transaction.phone_number)
    
    # Calculate risk score
    risk_score = 0
    status = "approved"
    message = "Transaction approved"
    
    if sim_swap_detected:
        risk_score += 60
    
    if transaction.amount > 1000:
        risk_score += 30
    elif transaction.amount > 500:
        risk_score += 20
    
    if transaction.is_new_recipient:
        risk_score += 15
    
    if sim_swap_detected and transaction.amount > 500:
        risk_score += 25
    
    # Make decision
    if risk_score >= 70:
        status = "blocked"
        message = f"Transaction blocked: {sim_message}"
    elif risk_score >= 40:
        status = "flagged"
        message = f"Manual review needed: {sim_message}"
    else:
        status = "approved"
        message = "Transaction approved - no fraud detected"
    
    return TransactionResponse(
        id=str(uuid.uuid4())[:8],
        phone_number=transaction.phone_number,
        amount=transaction.amount,
        currency=transaction.currency,
        status=status,
        risk_score=risk_score,
        message=message
    )

@app.get("/api/dashboard/stats")
async def get_stats():
    return {
        "total_transactions": 42,
        "blocked": 8,
        "approved": 30,
        "flagged": 4,
        "approval_rate": 71.4,
        "fraud_alerts": 12,
        "total_amount_saved": 4000
    }

@app.get("/api/dashboard/timeline")
async def get_timeline():
    return [
        {"date": "2024-01-01", "total": 5, "blocked": 1, "approved": 4},
        {"date": "2024-01-02", "total": 8, "blocked": 2, "approved": 6},
        {"date": "2024-01-03", "total": 12, "blocked": 3, "approved": 9},
        {"date": "2024-01-04", "total": 7, "blocked": 1, "approved": 6},
        {"date": "2024-01-05", "total": 10, "blocked": 1, "approved": 9},
    ]

@app.get("/api/fraud/alerts")
async def get_alerts():
    return [
        {
            "id": 1,
            "phone_number": "+99999991000",
            "risk_level": "critical",
            "alert_type": "sim_swap",
            "action_taken": "blocked",
            "created_at": "2024-01-05T10:30:00",
            "ai_analysis": {
                "explanation": "SIM swap detected 2 hours before high-value transaction",
                "decision": "BLOCK"
            }
        }
    ]