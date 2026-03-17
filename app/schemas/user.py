from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True

class UserLogin(SQLModel):
    email: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str