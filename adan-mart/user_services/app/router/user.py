from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.auth import EXPIRY_TIME, authenticate_user, create_access_token, current_user, hashed_password, oauth2_scheme
from app.auth import get_user_from_db, hashed_password
from app.database import get_session
from app.models import Register_User, Users


user_router = APIRouter(
    prefix= "/user",
    tags = ["user"],
    responses= {404: {"description": "User Not found"}},
)


@user_router.post("/register")
async def register_user(new_data : Annotated[Register_User, Depends()], 
                        session : Annotated[Session, Depends(get_session)],
                        ):
    db_user = get_user_from_db(session, new_data.username,
                                new_data.email 
                                )
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = Users(username=new_data.username,
                 email=new_data.email,
                 hash_password=hashed_password(new_data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": f""" User {user.username} has been registered"""}

@user_router.post("/token")
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)]):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expire_time =timedelta(minutes=EXPIRY_TIME)
    access_token = create_access_token({"sub": form_data.username}, expire_time)
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/user")
async def profile(current_user: Annotated[Users, Depends(current_user)]):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "id": current_user.id,
    }