# app/crud/user.py
from sqlmodel import Session, select
from app.models.user import UserCreate
from app.models.post import User
from typing import Optional

def create_user(session: Session, user: UserCreate) -> User:
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_users(session: Session) -> list[User]:
    return session.exec(select(User)).all()

def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def update_user(session: Session, user_id: int, user_update: UserCreate) -> User | None:
    db_user = session.get(User, user_id)
    if db_user:
        user_data = user_update.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user

def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False