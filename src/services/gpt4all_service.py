from pyllamacpp.model import Model
from src.config import Settings
from src.utils.logger import get_logger
from src.utils.exceptions import ModelLoadError
import asyncio

class GPT4ALLService:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GPT4ALLService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the GPT-4ALL model"""
        self.logger = get_logger(__name__)
        self.settings = Settings()
        self._load_model()

    def _load_model(self):
        """Load the GPT-4ALL model"""
        try:
            if not self._model:
                self.logger.info("Loading GPT-4ALL model...")
                self._model = Model(
                    model_path=self.settings.MODEL_PATH,
                    n_ctx=2048
                )
                self.logger.info("Model loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise ModelLoadError("Failed to load GPT-4ALL model")

    def is_model_loaded(self) -> bool:
        """Check if the model is loaded"""
        return self._model is not None

    async def generate(self, prompt: str) -> str:
        """Generate code based on prompt"""
        if not self.is_model_loaded():
            raise ModelLoadError("Model not loaded")

        try:
            # Run the generation in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._model.generate,
                prompt,
                self.settings.MAX_TOKENS,
                self.settings.TEMPERATURE
            )
            return response.strip()
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise Exception("Failed to generate response")
