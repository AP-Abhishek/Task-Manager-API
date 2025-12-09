from pydantic import BaseModel

class TaskSchema(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False