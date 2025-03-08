from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application settings
    DEBUG: bool = False
    
    # Security settings
    CORS_ORIGINS: List[str] = ["http://localhost:5000"]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # GPT4ALL settings
    MODEL_PATH: str = os.getenv("GPT4ALL_MODEL_PATH", "models/gpt4all-lora-quantized.bin")
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    
    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
