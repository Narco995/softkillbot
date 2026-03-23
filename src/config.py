import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """Application configuration"""
    
    # Telegram Bot
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    BOT_USERNAME: str = "Softkillbot"
    
    # RESTHeart Cloud
    RESTHEART_BASE_URL: str = "https://fba46a.us-east-1-free-1.restheart.com"
    RESTHEART_JWT_TOKEN: str = os.getenv("RESTHEART_JWT_TOKEN", "")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./softkillbot.db"
    )
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Features
    MAX_FILE_SIZE_MB: int = 50
    MAX_DOCUMENT_LENGTH: int = 100000
    
    class Config:
        env_file = ".env"

settings = Settings()