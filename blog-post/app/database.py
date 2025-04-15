# app/database.py
from sqlmodel import create_engine, SQLModel

# DATABASE_URL = "sqlite:///blog.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)