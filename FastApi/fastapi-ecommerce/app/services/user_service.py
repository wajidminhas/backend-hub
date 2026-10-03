


from typing import Annotated

from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session 

from app.dependencies import DbSession, get_db
from app.models.user import User
import logging

from app.schemas.users.user import UserCreate


logger = logging.getLogger("backend-service")

# def validateEmail(email_to_check: str, db: DbSession):
    
    
    # """here we are going to validate email that is provided email exist or not """
    
    # try:
    #     email_query = select(User).where(User.email == email_to_check)
    #     result = db.execute(email_query).scalar_one_or_none
    #     return result is not None
    
    # except SQLAlchemyError as db_error:
    #     logger.error(f"database error during validation, {str(db_error)}")  
                
    #     raise ("database error during validation") from db_error  
    
    
    
    
    
#*****************************email checker ******************

async def email_to_check(email: UserCreate, db : DbSession):
    
    try:
        statement_of_mail = select(User).where(User.email == email)
        result = db.execute(statement_of_mail).scalar_one_or_none
        return result is not None
    
    except HTTPException as error:
        raise 

# ************************** HASH PASSWORD ***************************

pwd_context = CryptContext(schemes=("bcrypt"))




def hash_Password(password):
    """here we are going to hash the password"""
    return pwd_context.hash(password)

def verifyPassword(password, hash_assword):
    """here we are going to verify the password"""
    return pwd_context.verify(password, hash_assword)


    
    