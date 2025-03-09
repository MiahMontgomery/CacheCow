from fastapi import APIRouter, HTTPException
from src.models.request_models import GenerateRequest, ProjectRequest
from src.models.response_models import HealthResponse, GenerateResponse, StatusResponse
from src.utils.logger import get_logger
from src.utils.exceptions import ModelLoadError
from src.services.service_container import get_gpt_service

router = APIRouter(tags=["API"])  # Add tags for better documentation organization

logger = get_logger(__name__)

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check endpoint called")
    return HealthResponse(status="ok")

@router.get("/status", response_model=StatusResponse)
async def get_status():
    """Get CacheCow Engine runtime status"""
    try:
        gpt_service = get_gpt_service()
        model_loaded = gpt_service and gpt_service.is_model_loaded()
        return StatusResponse(
            status="operational",
            model_loaded=model_loaded,
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Error checking status: {str(e)}")
        return StatusResponse(
            status="error",
            model_loaded=False,
            version="1.0.0",
            error=str(e)
        )

@router.post("/generate", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    """
    Generate code based on prompt

    Example request body:
    ```json
    {
        "prompt": "Write a Python hello world program"
    }
    ```
    """
    try:
        logger.info(f"Received generation request with prompt: {request.prompt}")

        gpt_service = get_gpt_service()
        if not gpt_service:
            raise ModelLoadError("GPT service not initialized")

        await gpt_service.ensure_initialized()  # Ensure model is loaded

        generated_code = await gpt_service.generate(request.prompt)
        logger.info("Successfully generated code response")

        return GenerateResponse(
            code=generated_code,
            status="success"
        )
    except ModelLoadError as e:
        logger.error(f"Model error: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Model error: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")

@router.post("/projects")
async def create_project(project: ProjectRequest):
    """Create a new project"""
    try:
        # Project creation logic would go here
        return {"status": "success", "message": "Project created successfully"}
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))