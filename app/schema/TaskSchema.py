from pydantic import BaseModel

class TaskSchema(BaseModel):
    name: str
    description: str | None = None
    completed: bool = False