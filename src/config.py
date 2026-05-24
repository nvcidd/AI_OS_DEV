"""
AI Operating System - Config Module
Handles environment variables and app configuration
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "AI Operating System"
    api_version: str = "0.1.0"
    
    # LLM - Groq (Free)
    groq_api_key: str  # Required, will raise error if not set
    groq_model: str = "mixtral-8x7b-32768"
    
    # Optional: OpenAI (for future use)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    
    # Database
    database_url: str = "sqlite:///./ai_os.db"
    
    # Environment
    environment: str = "development"  # development, staging, production
    debug: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # Allow extra environment variables


# Load settings
settings = Settings()