from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select
from jose import jwt, JWTError
from app.database import get_session
from app.models import TokenData,  Users
from dotenv import load_dotenv
import os


pwd_context = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables.")
ALGORITHM = "HS256"
EXPIRY_TIME = 30


def hashed_password(password):
    return pwd_context.hash(password)

# ***********         ********** VERIFY PASSWORD ************          ******************

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

# ***********         ********** REGISTER USER ************          ******************

def get_user_from_db(session : Annotated[Session, Depends(get_session)],
                     username : str, 
                     email: str | None = None):
    statement = select(Users).where(Users.username == username)
    user = session.exec(statement).first()
    if not user:
        statement = select(Users).where(Users.email == email)
        user = session.exec(statement).first()
        if user:
            return user
    return user
    
    
# ***********         ********** Authenticate User ************          ******************

def authenticate_user(session : Annotated[Session, Depends(get_session)],
                      username,
                      password
                      ):
    
         db_user = get_user_from_db(username=username, session=session)
         if not db_user:
             return False
         if not verify_password(password=password, hashed_password=db_user.hash_password):
             return False
         return db_user

# ***********         ********** CREATE ACCESS TOKEN ************          ******************

def create_access_token(data: dict, expiry_time : timedelta | None = None):
    encode_data = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    encode_data.update({"exp":expire})
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ***********         ********** DECODE ACCESS TOKEN / Current User ************          ******************

# def current_user(token : Annotated[str, Depends(oauth2_scheme)],
#                  session : Annotated[Session, Depends(get_session)]):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)

#     except:
#         raise JWTError
#     user = get_user_from_db(session=session, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# ***********         ********** DECODE ACCESS TOKEN / Current User ************          ******************
# This function is similar to the previous one but uses a different approach to handle the token.

def current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_from_db(session=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

