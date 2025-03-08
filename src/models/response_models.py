from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str

class GenerateResponse(BaseModel):
    code: str
    status: str

class StatusResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str
    error: Optional[str] = None
