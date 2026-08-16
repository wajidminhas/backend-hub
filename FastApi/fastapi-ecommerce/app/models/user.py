
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.database import Base

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique= True, index=True)
    fullname : Mapped[Optional[str]] = mapped_column(nullable=True)
    hashed_password : Mapped[str] = mapped_column(nullable=False)
    created_at : Mapped[Optional[str]] = mapped_column(nullable=True)
    

