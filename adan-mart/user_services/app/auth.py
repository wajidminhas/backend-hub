from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select
from starlette import status

from app.database import get_session
from app.models import CreateUserRequest, Users


router = APIRouter(
    prefix= "/auth",
    tags=['auth']
)


SECRET_KEY = "6bd169965f84fd4a9123b813535d399c7bed63e9a561b9b1dba391398a5220fc"  # openssl rand -hex 32
ALGORITHIM = "HS256"  # algorithm used to encode the JWT  


 # to encrypt / hash the password
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto" )  


# to get the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")  


# this is a dependency that will be used to get the database session
db_dependency = Annotated[Session, Depends(get_session)] 


# here create user function will be used to create a user
# and return the user object
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependency, create_user_request: CreateUserRequest):
    # Check if username already exists
    existing_user = db.exec(select(Users).where(Users.username == create_user_request.username)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    new_user = Users(
        username=create_user_request.username,
        hash_password=bcrypt_context.hash(create_user_request.password)
    )
    # Add the new user to the database
    db.add(new_user)
    db.commit()
    # db.refresh(new_user)
    # return new_user
    


