from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    app_name: str = "Government Portal - Defacement Testing"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 9000
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:9000",
        "http://127.0.0.1:9000",
        "http://localhost:3000",
    ]
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_times: int = 100
    rate_limit_seconds: int = 60
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
