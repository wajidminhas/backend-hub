
from pydantic import BaseModel, EmailStr 
from datetime import datetime


class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str
    
    
    
class UserResponse(BaseModel):
    id: str
    email : EmailStr
    username : str
    created_at : datetime
    