from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict
from ..models.fraud_alert import AlertType, RiskLevel, ActionTaken

class FraudAlertResponse(BaseModel):
    id: int
    transaction_id: Optional[int]
    phone_number: str
    alert_type: AlertType
    risk_level: RiskLevel
    camara_checks: Dict
    ai_analysis: Dict
    action_taken: ActionTaken
    created_at: datetime
    
    class Config:
        from_attributes = True