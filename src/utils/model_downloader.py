import os
import requests
from tqdm import tqdm
from src.config import Settings
from src.utils.logger import get_logger
from src.utils.exceptions import ModelLoadError

logger = get_logger(__name__)

def download_model():
    """Download the GPT4ALL model if it doesn't exist"""
    settings = Settings()
    model_path = settings.MODEL_PATH

    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Remove incomplete/corrupted model file if it exists
    if os.path.exists(model_path):
        os.remove(model_path)
        logger.info("Removed existing model file for fresh download")

    # Use a stable, direct download URL for GGUF model
    url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_0.gguf"

    try:
        logger.info(f"Downloading model from {url}")
        logger.info("Attempting to download without auth...")

        # Stream with a longer timeout and larger chunk size
        response = requests.get(url, stream=True, timeout=1800)  # 30 minute timeout

        # Log response details for debugging
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")

        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        logger.info(f"Expected model size: {total_size / 1024 / 1024:.2f} MB")

        if total_size < 500_000_000:  # Less than 500MB
            raise ModelLoadError("Model file size is suspiciously small")

        # Download with progress bar and verification
        with open(model_path, 'wb') as f, tqdm(
            desc="Downloading model",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            downloaded_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                size = f.write(chunk)
                pbar.update(size)
                downloaded_size += size
                if downloaded_size % (100 * 1024 * 1024) == 0:  # Log every 100MB
                    logger.info(f"Downloaded {downloaded_size / 1024 / 1024:.2f} MB of {total_size / 1024 / 1024:.2f} MB")

        # Verify the downloaded file
        actual_size = os.path.getsize(model_path)
        logger.info(f"Downloaded size: {actual_size / 1024 / 1024:.2f} MB")

        if actual_size != total_size:
            raise ModelLoadError(
                f"Downloaded file size ({actual_size}) does not match expected size ({total_size})"
            )

        logger.info(f"Model downloaded and verified successfully at {model_path}")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error downloading model: {str(e)}")
        if os.path.exists(model_path):
            os.remove(model_path)
        raise ModelLoadError(f"Failed to download model: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during model download: {str(e)}")
        if os.path.exists(model_path):
            os.remove(model_path)
        raise ModelLoadError(f"Unexpected error during model download: {str(e)}")