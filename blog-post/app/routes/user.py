# app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import engine
from app.models.user import  UserCreate, UserUpdate
from app.crud.user import create_user, get_users, get_user, update_user, delete_user
from typing import List
from app.models.post import User  # Import the User model


router = APIRouter(prefix="/users", tags=["Users"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=User)
def create_user_route(user: UserCreate, session: Session = Depends(get_session)):
    return create_user(session, user)

@router.get("/", response_model=List[User])
def read_users(session: Session = Depends(get_session)):
    return get_users(session)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=User)
def update_user_route(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = update_user(session, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user_route(user_id: int, session: Session = Depends(get_session)):
    success = delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}