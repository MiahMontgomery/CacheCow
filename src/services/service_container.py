"""Container for global service instances"""
from typing import Optional
from src.services.gpt4all_service import GPT4ALLService

# Global GPT4ALL service instance
gpt_service: Optional[GPT4ALLService] = None

def init_gpt_service() -> GPT4ALLService:
    """Initialize the GPT4ALL service"""
    global gpt_service
    if gpt_service is None:
        gpt_service = GPT4ALLService()
    return gpt_service

def get_gpt_service() -> Optional[GPT4ALLService]:
    """Get the GPT4ALL service instance"""
    global gpt_service
    if gpt_service is None:
        gpt_service = GPT4ALLService()
    return gpt_service