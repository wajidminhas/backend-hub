from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.auth import EXPIRY_TIME, authenticate_user, create_access_token, create_refresh_token, current_user, hashed_password, oauth2_scheme, validate_refresh_token, verify_password
from app.auth import get_user_from_db, hashed_password
from app.database import get_session
from app.models import PasswordUpdate, Register_User, Token, Users


user_router = APIRouter(
    prefix="/user",
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

#     ********** LOGIN USER ************

@user_router.post("/token")
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)]):
    user = authenticate_user(session, form_data.username,  form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expire_time =timedelta(minutes=EXPIRY_TIME)
    access_token = create_access_token({"sub": form_data.username}, expire_time)

    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub": user.email}, refresh_expire_time)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

#     ********** GET USER PROFILE ************ 

@user_router.get("/user")
async def profile(current_user: Annotated[Users, Depends(current_user)]):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "id": current_user.id,
    }

#     ********** REFRESH TOKEN ************

@user_router.post("/token/refresh")
async def generate_refresh_token(old_token: str, session: Annotated[Session, Depends(get_session)]):
    # write credentials exception
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = validate_refresh_token(old_token, session)
    if not user:
        raise credentials_exception
    
    expire_time = timedelta(minutes=EXPIRY_TIME)
    access_token = create_access_token({"sub": user.username}, expire_time)
    
    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub": user.email}, refresh_expire_time)

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

#    ********** UPDATE USER PASSWORD ************

@user_router.put("/update_password")
async def update_password(current_user : Annotated[Users, Depends(current_user)],
                          password_data : Annotated[PasswordUpdate, Depends()],
                          session: Annotated[Session, Depends(get_session)]):
    db_user = get_user_from_db(session=session, username=current_user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    if not verify_password(password=password_data.current_password, hashed_password=db_user.hash_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    db_user.hash_password = hashed_password(password_data.new_password)
    session.add(db_user)
    session.commit()
    return {"message": f""" User {db_user.username}'s password has been updated""" }
                                                          