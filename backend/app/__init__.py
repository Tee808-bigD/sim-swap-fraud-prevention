from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Nokia Network as Code
    nac_api_key: str = ""
    
    # Anthropic
    anthropic_api_key: str = ""
    
    # Database
    database_url: str = "sqlite:///./simguard.db"
    
    # App
    app_env: str = "development"
    cors_origins: str = "http://localhost:5173"
    
    # Number Verification OAuth
    nac_auth_clientcredentials_url: str = "https://nac-authorization-server.p-eu.rapidapi.com"
    nac_auth_clientcredentials_host: str = "nac-authorization-server.nokia.rapidapi.com"
    nac_wellknown_metadata_url: str = "https://well-known-metadata.p-eu.rapidapi.com"
    nac_wellknown_metadata_host: str = "well-known-metadata.nokia.rapidapi.com"
    nac_number_verification_url: str = "https://number-verification.p-eu.rapidapi.com"
    nac_number_verification_host: str = "number-verification.nokia.rapidapi.com"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()