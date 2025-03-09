from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import asyncio

from src.routes.api import router
from src.utils.logger import setup_logger, get_logger
from src.utils.exceptions import CacheCowException
from src.services.service_container import init_gpt_service
from src.config import Settings

# Initialize logger
logger = setup_logger()

# Load settings
settings = Settings()

# Initialize FastAPI app with explicit root path
app = FastAPI(
    title="CacheCow Engine",
    description="A backend system for autonomous software generation using GPT-4ALL",
    version="1.0.0",
    docs_url="/",  # Make docs the root URL
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Initialize GPT4ALL service during startup
        logger.info("Initializing GPT4ALL service...")
        service = init_gpt_service()
        # Start model initialization in background
        asyncio.create_task(service.ensure_initialized())
        logger.info("GPT4ALL service initialization started in background")
    except Exception as e:
        logger.error(f"Error initializing GPT4ALL service: {str(e)}")
        # Let the service endpoints handle the absence of the model

# Include API routes
app.include_router(router)

@app.exception_handler(CacheCowException)
async def cachecow_exception_handler(request: Request, exc: CacheCowException):
    logger.error(f"CacheCow error: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request parameters"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    # ALWAYS serve on port 5000 and bind to all interfaces
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        reload=settings.DEBUG
    )