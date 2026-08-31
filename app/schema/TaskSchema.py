from pydantic import BaseModel, Field

class TaskSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Task title (max 100 characters)")
    description: str | None = Field(default=None, max_length=500, description="Optional description (max 500 characters)")
    completed: bool = False

class TaskUpdateSchema(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100, description="Optional task title")
    description: str | None = Field(default=None, max_length=500, description="Optional description")
    completed: bool | None = Field(default=None, description="Optional completion status")
