# app/database.py
from sqlmodel import create_engine, SQLModel
from sqlmodel import Session

from app import settings
from app.settings import DATABASE_URL
# DATABASE_URL = "sqlite:///blog.db"

connectin_string = str (settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connectin_string, echo=True)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_session():
    
    return Session(engine)