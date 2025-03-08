import os
import requests
from tqdm import tqdm
from src.config import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

def download_model():
    """Download the GPT4ALL model if it doesn't exist"""
    settings = Settings()
    model_path = settings.MODEL_PATH
    
    if os.path.exists(model_path):
        logger.info(f"Model already exists at {model_path}")
        return
        
    logger.info("Downloading GPT4ALL model...")
    
    # GPT4ALL model URL
    url = "https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin"
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    with open(model_path, 'wb') as f, tqdm(
        desc=model_path,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)
            
    logger.info(f"Model downloaded successfully to {model_path}")
