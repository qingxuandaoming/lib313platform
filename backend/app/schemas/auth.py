from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True