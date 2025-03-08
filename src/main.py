from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError

from src.routes.api import router
from src.utils.logger import setup_logger
from src.utils.exceptions import CacheCowException
from src.config import Settings

# Initialize logger
logger = setup_logger()

# Load settings
settings = Settings()

# Initialize FastAPI app
app = FastAPI(
    title="CacheCow Engine",
    description="A backend system for autonomous software generation using GPT-4ALL",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # More permissive for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # More permissive for development
)

# Include API routes with the correct prefix
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """Redirect root to API documentation"""
    logger.info("Root endpoint accessed, redirecting to API docs")
    return RedirectResponse(url="/api/docs")

@app.exception_handler(CacheCowException)
async def cachecow_exception_handler(request, exc):
    logger.error(f"CacheCow error: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request parameters"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=5000,
        reload=settings.DEBUG
    )