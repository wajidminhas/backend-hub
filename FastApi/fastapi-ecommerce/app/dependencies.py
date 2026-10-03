





from typing import Annotated, Generator

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    
    with SessionLocal() as session:
        
        try:
            yield session
        except Exception:
            session.roll_back()
            raise
    
DbSession = Annotated[Session, Depends(get_db)]