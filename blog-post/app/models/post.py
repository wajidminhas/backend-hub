# app/models/post.py
from sqlmodel import SQLModel, Field
from typing import Optional

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")

class PostCreate(SQLModel):
    title: str
    content: str
    author_id: int

class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author_id: Optional[int] = None