from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="The prompt for code generation")
    
class ProjectRequest(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    template: str = Field(..., description="Project template to use")
