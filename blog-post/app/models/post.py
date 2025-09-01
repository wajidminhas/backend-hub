# app/models/post.py
from typing import Optional
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    
    # Relationship: One user can have many posts
    posts: List["Post"] = Relationship(back_populates="author")



class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int | None = Field(default=None, foreign_key="user.id")  # Assuming a User model exists)

    author: User | None = Relationship(back_populates="posts")

class PostCreate(SQLModel):
    title: str
    content: str
    author_id: Optional[int] = None

class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author_id: Optional[int] = None