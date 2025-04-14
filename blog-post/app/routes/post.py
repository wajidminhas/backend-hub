# app/routes/post.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import engine
from app.models.post import Post, PostCreate, PostUpdate
from app.crud.post import create_post, get_posts, get_post, update_post, delete_post
from typing import List

router = APIRouter(prefix="/posts", tags=["Posts"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=Post)
def create_post_route(post: PostCreate, session: Session = Depends(get_session)):
    return create_post(session, post)

@router.get("/", response_model=List[Post])
def read_posts(session: Session = Depends(get_session)):
    return get_posts(session)

@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, session: Session = Depends(get_session)):
    post = get_post(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch("/{post_id}", response_model=Post)
def update_post_route(post_id: int, post_update: PostUpdate, session: Session = Depends(get_session)):
    post = update_post(session, post_id, post_update)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{post_id}")
def delete_post_route(post_id: int, session: Session = Depends(get_session)):
    success = delete_post(session, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted"}