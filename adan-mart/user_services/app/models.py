
from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class Users(SQLModel):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(default="")
    hash_password: str = Field(default="")
    is_active: bool = Field(default=True)



class CreateUserRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str