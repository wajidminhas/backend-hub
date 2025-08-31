# app/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional

# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     username: str = Field(unique=True)
#     email: str = Field(unique=True)

class UserCreate(SQLModel):
    username: str
    email: str

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None