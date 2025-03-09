from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application settings
    DEBUG: bool = False

    # Security settings
    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]

    # GPT4ALL settings
    MODEL_DIR: str = os.getenv("GPT4ALL_MODEL_DIR", "models")
    MODEL_NAME: str = "llama-2-7b-chat.Q4_0.gguf"  # Using GGUF format for GPU support
    MODEL_PATH: str = os.path.join(MODEL_DIR, MODEL_NAME)
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    N_THREADS: int = 4  # Using more threads for GPU acceleration

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"