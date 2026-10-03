


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.users.user import UserCreate
from app.services.user_service import validateEmail
# from app.services.user_service import create_user
import logging

logger = logging.getLogger("fastapi backend")

router = APIRouter()


@router.post("/register")
def user_register(payload : UserCreate, db: Session = Depends(get_db)):
    """here we are going to register user"""
    
    
    try:
        email_exists = validateEmail(email_to_check=payload.email, db=db)
        if email_exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        return {"message": "Email is available for registration.", "available": True}
            
    
    except RuntimeError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error during email validation.")
        
    except Exception as unexpected_err:
        logger.critical(f"unexpected operation failure {str(unexpected_err)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="something wrong on our end.")