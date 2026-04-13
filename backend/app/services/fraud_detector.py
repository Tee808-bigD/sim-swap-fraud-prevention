"""Rule-based fraud detection engine."""
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from .camara import camara_service

logger = logging.getLogger(__name__)

class FraudDetector:
    def __init__(self):
        self.weights = {
            "sim_swap_24h": 60,
            "sim_swap_7d": 40,
            "device_swap": 30,
            "number_not_verified": 25,
            "high_value_500": 20,
            "high_value_1000": 30,
            "new_recipient": 15,
            "sim_swap_high_value": 25,
            "sim_swap_new_recipient": 20,
        }
    
    async def compute_risk_score(self, transaction: Dict[str, Any], history: Optional[list] = None) -> Dict[str, Any]:
        """Compute risk score based on transaction and CAMARA checks."""
        score = 0
        factors = []
        
        phone = transaction.get("phone_number")
        sim_swap_detected, swap_date = await camara_service.check_sim_swap(phone)
        device_swap_detected, device_date = await camara_service.check_device_swap(phone)
        
        # SIM swap checks
        if sim_swap_detected and swap_date:
            try:
                swap_time = datetime.fromisoformat(swap_date.replace('Z', '+00:00'))
                hours_since_swap = (datetime.now().astimezone() - swap_time).total_seconds() / 3600
                
                if hours_since_swap <= 24:
                    score += self.weights["sim_swap_24h"]
                    factors.append("SIM swap within 24 hours")
                elif hours_since_swap <= 168:
                    score += self.weights["sim_swap_7d"]
                    factors.append("SIM swap within 7 days")
            except:
                score += self.weights["sim_swap_24h"]
                factors.append("SIM swap detected")
        
        if device_swap_detected:
            score += self.weights["device_swap"]
            factors.append("Device swap detected")
        
        # Amount checks
        amount = transaction.get("amount", 0)
        if amount > 1000:
            score += self.weights["high_value_1000"]
            factors.append(f"High-value transaction: ${amount}")
        elif amount > 500:
            score += self.weights["high_value_500"]
            factors.append(f"Medium-value transaction: ${amount}")
        
        # New recipient check
        if transaction.get("is_new_recipient", False):
            score += self.weights["new_recipient"]
            factors.append("New recipient")
        
        # Composite risks
        if sim_swap_detected and amount > 500:
            score += self.weights["sim_swap_high_value"]
            factors.append("SIM swap + high value transaction")
        
        if sim_swap_detected and transaction.get("is_new_recipient", False):
            score += self.weights["sim_swap_new_recipient"]
            factors.append("SIM swap + new recipient")
        
        if score >= 80:
            risk_level = "critical"
        elif score >= 60:
            risk_level = "high"
        elif score >= 30:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_score": min(score, 100),
            "risk_level": risk_level,
            "factors": factors,
            "sim_swap_detected": sim_swap_detected,
            "device_swap_detected": device_swap_detected,
            "swap_date": swap_date,
        }

fraud_detector = FraudDetector()