"""Nokia CAMARA API integration - SIM Swap, Device Swap via Network as Code SDK."""
import logging
from datetime import datetime, timedelta
from typing import Tuple, Optional
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Test numbers from Nokia documentation
TEST_NUMBERS = {
    "swap_occurred": "+99999991000",
    "no_swap": "+99999991001",
}

class CamaraService:
    def __init__(self):
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize Nokia Network as Code client"""
        if settings.nac_api_key and settings.nac_api_key not in ["", "your-rapidapi-key-here"]:
            try:
                from network_as_code import NetworkAsCodeClient
                self.client = NetworkAsCodeClient(
                    token=settings.nac_api_key,
                    rapidapi_key=settings.nac_api_key
                )
                logger.info("CAMARA client initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize CAMARA client: {e}")
                self.client = None
        else:
            logger.info("No API key provided, using demo mode")
    
    async def check_sim_swap(self, phone_number: str, max_age_hours: int = 24) -> Tuple[bool, Optional[str]]:
        """Check if SIM swap occurred within time window."""
        if not self.client:
            return self._demo_sim_check(phone_number)
        
        try:
            sim_swap = self.client.sim_swap
            result = await sim_swap.check(phone_number, max_age_hours=max_age_hours)
            return result.swap_occurred, result.swap_date
        except Exception as e:
            logger.error(f"SIM swap check failed: {e}")
            return False, None
    
    def _demo_sim_check(self, phone_number: str) -> Tuple[bool, Optional[str]]:
        """Demo mode using Nokia test numbers"""
        if phone_number == TEST_NUMBERS["swap_occurred"]:
            return True, (datetime.now() - timedelta(hours=2)).isoformat()
        return False, None
    
    async def check_device_swap(self, phone_number: str, max_age_hours: int = 240) -> Tuple[bool, Optional[str]]:
        """Check if device swap occurred within time window."""
        if not self.client:
            return self._demo_device_check(phone_number)
        
        try:
            device_swap = self.client.device_swap
            result = await device_swap.check(phone_number, max_age_hours=max_age_hours)
            return result.swap_occurred, result.swap_date
        except Exception as e:
            logger.error(f"Device swap check failed: {e}")
            return False, None
    
    def _demo_device_check(self, phone_number: str) -> Tuple[bool, Optional[str]]:
        """Demo device swap check"""
        if phone_number == TEST_NUMBERS["swap_occurred"]:
            return True, (datetime.now() - timedelta(days=2)).isoformat()
        return False, None

camara_service = CamaraService()