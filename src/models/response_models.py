from pydantic import BaseModel, Field
from typing import Optional

class HealthResponse(BaseModel):
    status: str = Field(
        default="ok",
        description="Health check status",
        example="ok"
    )

class GenerateResponse(BaseModel):
    code: str = Field(
        description="Generated code output",
        example="def hello_world():\n    print('Hello, World!')"
    )
    status: str = Field(
        default="success",
        description="Generation status",
        example="success"
    )

class StatusResponse(BaseModel):
    status: str = Field(
        description="Current system status",
        example="operational"
    )
    model_loaded: bool = Field(
        description="Whether the GPT4ALL model is loaded",
        example=True
    )
    version: str = Field(
        description="CacheCow Engine version",
        example="1.0.0"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if any",
        example="Model failed to load"
    )