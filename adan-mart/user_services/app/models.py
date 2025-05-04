
from typing import Annotated
from fastapi import Form
from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username : str
    email: str 
    hash_password: str
    # is_active: bool = Field(default=True)



# class CreateUserRequest(BaseModel):
#     email: str
#     username : str
#     password: str

class Register_User(BaseModel):
    email: Annotated[
        str,
        Field(
            max_length=20,
        ),
        Form()
    ]

    password: Annotated[
        str,
        Field(
            min_length=8,
        ),
        Form()
    ]
    username: Annotated[
        str,
        Field(
            max_length=20,
        ),
        Form()
    ]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None