import logging
import sys
from src.config import Settings

def setup_logger():
    """Set up the application logger"""
    settings = Settings()
    
    # Create logger
    logger = logging.getLogger("cachecow")
    logger.setLevel(settings.LOG_LEVEL)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger

def get_logger(name: str):
    """Get a logger instance"""
    return logging.getLogger(f"cachecow.{name}")
