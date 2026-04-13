"""Agentic AI engine using Anthropic Claude for fraud decisions."""
import logging
import json
from typing import Dict, Any
from anthropic import Anthropic
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

SYSTEM_PROMPT = """You are SimGuard AI, an expert fraud detection system for African mobile money.

Your role is to analyze transaction data and CAMARA API results to detect SIM swap fraud.

FRAUD PATTERNS TO DETECT:
1. Recent SIM swap (within 24-48 hours) + high-value transaction = CRITICAL risk
2. SIM swap + new/unusual recipient = HIGH risk  
3. Device swap + large amount = MEDIUM risk

OUTPUT FORMAT (JSON only):
{
    "decision": "BLOCK" | "APPROVE" | "FLAG_FOR_REVIEW",
    "confidence": 0-100,
    "explanation": "Clear explanation for agents",
    "recommended_actions": ["action1", "action2"],
    "fraud_probability": 0-100
}
"""

class AIFraudEngine:
    def __init__(self):
        self.client = None
        if settings.anthropic_api_key and settings.anthropic_api_key not in ["", "sk-ant-placeholder"]:
            self.client = Anthropic(api_key=settings.anthropic_api_key)
            logger.info("Claude AI engine initialized")
        else:
            logger.info("No Anthropic API key, using rule-based fallback")
    
    async def analyze_fraud_risk(self, transaction: Dict[str, Any], risk_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze fraud risk using Claude AI or fallback to rules."""
        if not self.client:
            return self._fallback_decision(risk_analysis)
        
        prompt = self._build_prompt(transaction, risk_analysis)
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.2,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            result = json.loads(response.content[0].text)
            return result
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._fallback_decision(risk_analysis)
    
    def _build_prompt(self, transaction: Dict[str, Any], risk_analysis: Dict[str, Any]) -> str:
        return f"""Analyze this transaction for SIM swap fraud:

TRANSACTION DETAILS:
- Phone: {transaction.get('phone_number')}
- Amount: {transaction.get('currency', 'KES')} {transaction.get('amount')}
- Type: {transaction.get('transaction_type')}
- Recipient: {transaction.get('recipient', 'Unknown')}
- New Recipient: {transaction.get('is_new_recipient', False)}

CAMARA RESULTS:
- SIM Swap Detected: {risk_analysis.get('sim_swap_detected', False)}
- Risk Score: {risk_analysis.get('risk_score', 0)}
- Risk Level: {risk_analysis.get('risk_level', 'unknown')}
- Factors: {', '.join(risk_analysis.get('factors', []))}

Make a decision: BLOCK, APPROVE, or FLAG_FOR_REVIEW."""
    
    def _fallback_decision(self, risk_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based fallback when AI is unavailable"""
        risk_level = risk_analysis.get("risk_level", "low")
        score = risk_analysis.get("risk_score", 0)
        
        if risk_level == "critical" or score >= 80:
            return {
                "decision": "BLOCK",
                "confidence": 90,
                "explanation": "Critical risk detected: Recent SIM swap combined with high-value transaction.",
                "recommended_actions": ["Contact customer via alternative channel", "Request in-person verification"],
                "fraud_probability": 95
            }
        elif risk_level == "high" or score >= 60:
            return {
                "decision": "FLAG_FOR_REVIEW",
                "confidence": 75,
                "explanation": "High risk: Suspicious patterns detected. Manual review recommended.",
                "recommended_actions": ["Verify customer identity", "Check transaction history"],
                "fraud_probability": 70
            }
        else:
            return {
                "decision": "APPROVE",
                "confidence": 85,
                "explanation": "Low risk: No suspicious patterns detected.",
                "recommended_actions": ["Process transaction"],
                "fraud_probability": 10
            }

ai_engine = AIFraudEngine()