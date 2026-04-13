from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict

class SimCheckResponse(BaseModel):
    id: int
    phone_number: str
    sim_swap_detected: bool
    swap_date: Optional[str]
    device_swap_detected: bool
    device_swap_date: Optional[str]
    number_verified: bool
    check_results: Dict
    created_at: datetime
    
    class Config:
        from_attributes = True