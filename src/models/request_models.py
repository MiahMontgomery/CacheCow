from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="The prompt for code generation",
        example="Write a Python hello world program"
    )

class ProjectRequest(BaseModel):
    name: str = Field(
        ...,
        description="Project name",
        example="my-awesome-project"
    )
    description: str = Field(
        ...,
        description="Project description",
        example="A Python project that does amazing things"
    )
    template: str = Field(
        ...,
        description="Project template to use",
        example="python-fastapi"
    )