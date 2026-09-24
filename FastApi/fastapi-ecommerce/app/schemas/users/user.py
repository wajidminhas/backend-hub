
from pydantic import BaseModel 
from datetime import datetime


class UserCreate(BaseModel):
    username : str
    email : str
    password : str
    
    
    
class UserResponse(BaseModel):
    id: str
    email : str
    username : str
    created_at : datetime
    