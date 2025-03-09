import os
import asyncio
from gpt4all import GPT4All
from src.config import Settings
from src.utils.logger import get_logger
from src.utils.exceptions import ModelLoadError
from src.utils.model_downloader import download_model

class GPT4ALLService:
    _instance = None
    _model = None
    _initialization_lock = None
    _is_initializing = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GPT4ALLService, cls).__new__(cls)
            cls._instance.logger = get_logger(__name__)
            cls._instance.settings = Settings()
            cls._instance._initialization_lock = asyncio.Lock()
        return cls._instance

    async def ensure_initialized(self):
        """Ensure the model is initialized"""
        if self._model is not None:
            return

        if self._is_initializing:
            self.logger.info("Model initialization already in progress")
            return

        async with self._initialization_lock:
            if self._model is not None:  # Double-check after acquiring lock
                return

            self._is_initializing = True
            try:
                self.logger.info("Starting GPT4ALL service initialization")
                await self._ensure_model()
                await self._load_model()
                self.logger.info("GPT4ALL service initialization completed successfully")
            except ModelLoadError as e:
                self.logger.error(f"Failed to initialize GPT4ALL service: {str(e)}")
                raise
            except Exception as e:
                self.logger.error(f"An unexpected error occurred during initialization: {str(e)}")
                raise ModelLoadError(f"An unexpected error occurred during GPT4ALL service initialization: {str(e)}")
            finally:
                self._is_initializing = False

    async def _ensure_model(self):
        """Ensure the model file exists and is valid"""
        try:
            os.makedirs(self.settings.MODEL_DIR, exist_ok=True)
            self.logger.info(f"Created/verified model directory at {self.settings.MODEL_DIR}")

            model_path = self.settings.MODEL_PATH
            self.logger.info(f"Checking for model at {model_path}")

            if not os.path.exists(model_path):
                self.logger.info("Model file not found. Starting download...")
                await asyncio.to_thread(download_model)
                self.logger.info("Model download completed successfully")
            else:
                file_size = os.path.getsize(model_path)
                self.logger.info(f"Found existing model file of size {file_size / 1024 / 1024:.2f} MB")
                if file_size < 100_000_000:  # Less than 100MB
                    self.logger.warning(f"Existing model file is too small ({file_size} bytes)")
                    self.logger.info("Redownloading model...")
                    await asyncio.to_thread(download_model)
                else:
                    self.logger.info(f"Using existing model at {model_path}")
        except Exception as e:
            self.logger.error(f"Error ensuring model file: {str(e)}")
            raise ModelLoadError(f"Error ensuring model file: {str(e)}")

    async def _load_model(self):
        """Load the GPT-4ALL model"""
        try:
            self.logger.info("Loading GPT-4ALL model...")
            model_dir = self.settings.MODEL_DIR
            model_name = self.settings.MODEL_NAME

            self.logger.debug(f"Model directory: {model_dir}")
            self.logger.debug(f"Model name: {model_name}")

            # Enable GPU mode by removing CPU-only restrictions
            if "CUDA_VISIBLE_DEVICES" in os.environ:
                del os.environ["CUDA_VISIBLE_DEVICES"]

            # Load model in a thread pool to avoid blocking
            self._model = await asyncio.to_thread(
                lambda: GPT4All(
                    model_name=model_name,
                    model_path=model_dir,
                    allow_download=False,  # We handle downloads separately
                    n_threads=self.settings.N_THREADS
                )
            )
            self.logger.info("Model loaded successfully with GPU support")
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise ModelLoadError(f"Failed to load GPT-4ALL model: {str(e)}")

    def is_model_loaded(self) -> bool:
        """Check if the model is loaded"""
        return self._model is not None

    async def generate(self, prompt: str) -> str:
        """Generate code based on prompt"""
        await self.ensure_initialized()

        if not self.is_model_loaded():
            raise ModelLoadError("Model not loaded")

        try:
            full_prompt = f"""Write code for the following request:
{prompt}

Return only the code without explanations:
"""
            response = await asyncio.to_thread(
                lambda: self._model.generate(
                    full_prompt,
                    max_tokens=self.settings.MAX_TOKENS,
                    temp=self.settings.TEMPERATURE,
                    top_k=40,
                    top_p=0.9,
                    repeat_penalty=1.1
                )
            )

            if not response or not response.strip():
                raise Exception("Empty response from model")

            code = response.strip()
            return code

        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")

    def __del__(self):
        """Cleanup when service is destroyed"""
        if self._model:
            self.logger.info("Cleaning up GPT-4ALL model resources")
            del self._model