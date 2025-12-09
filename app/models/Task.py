from pydantic import BaseModel

class Task(BaseModel):
    id: str
    name: str
    description: str | None = None
    completed: bool = False