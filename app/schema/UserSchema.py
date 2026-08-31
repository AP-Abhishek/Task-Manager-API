from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    password: str = Field(..., min_length=4, max_length=100, description="Password (min 4 characters)")