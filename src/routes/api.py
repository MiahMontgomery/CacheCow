from fastapi import APIRouter, HTTPException, Depends
from src.models.request_models import GenerateRequest, ProjectRequest
from src.models.response_models import HealthResponse, GenerateResponse, StatusResponse
from src.services.gpt4all_service import GPT4ALLService
from src.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check endpoint called")
    logger.info("Health check endpoint returning OK status")
    return HealthResponse(status="ok")

@router.get("/status", response_model=StatusResponse)
async def get_status():
    """Get CacheCow Engine runtime status"""
    try:
        gpt_service = GPT4ALLService()
        model_loaded = gpt_service.is_model_loaded()
        return StatusResponse(
            status="operational",
            model_loaded=model_loaded,
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Error checking status: {str(e)}")
        raise HTTPException(status_code=500, detail="Error checking system status")

@router.post("/generate", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    """Generate code based on prompt"""
    try:
        gpt_service = GPT4ALLService()
        generated_code = await gpt_service.generate(request.prompt)
        return GenerateResponse(
            code=generated_code,
            status="success"
        )
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating code")

@router.post("/projects")
async def create_project(project: ProjectRequest):
    """Create a new project"""
    try:
        # Project creation logic would go here
        return {"status": "success", "message": "Project created successfully"}
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating project")