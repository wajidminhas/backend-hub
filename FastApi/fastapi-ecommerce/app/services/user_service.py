


from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.user import User
import logging


logger = logging.getLogger("backend-service")

def validateEmail(email_to_check: str, db : Session ):
    
    
    """here we are going to validate email that is provided email exist or not """
    
    try:
        email_query = select(User).where(User.email == email_to_check)
        result = db.execute(email_query).scalar_one_or_none
        return result is not None
    
    except SQLAlchemyError as db_error:
        logger.error(f"database error during validation, {str(db_error)}")  
                
        raise ("database error during validation") from db_error  