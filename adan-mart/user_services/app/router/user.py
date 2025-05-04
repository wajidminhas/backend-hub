from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.auth import authenticate_user, current_user, oauth2_scheme
from app.auth import get_user_from_db, hash_password
from app.database import get_session
from app.models import Register_User, Users


user_router = APIRouter(
    prefix= "/user",
    tags = ["user"],
    responses= {404: {"description": "User Not found"}},
)



@user_router.get("/profile/")
async def read_user_profile(current_user: Annotated[Users, Depends(current_user)]):
    return current_user

@user_router.post("/register")
async def register_user(new_data : Annotated[Register_User, Depends()], 
                        session : Annotated[Session, Depends(get_session)],
                        ):
    db_user = get_user_from_db(session, new_data.username,
                                new_data.email 
                                )
    if db_user:
        return HTTPException(status_code=400, detail="User already exists")
    user = Users(username=new_data.username, email=new_data.email, hash_password=hash_password(new_data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": f""" User {user.username} has been registered"""}

@user_router.get("/token")
async def user_profile(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], session : Annotated[Session, Depends(get_session)]):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        return HTTPException(status_code=400, detail="Invalid Credentials")
    return user
    

