# app/database.py
from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends
from app.settings import DATABASE_URL

# SQLite connection (no driver replacement needed)
connection_string = str(DATABASE_URL)

# Create engine (echo=True for debugging, disable in production)
engine = create_engine(connection_string, echo=True)

# Initialize tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency for FastAPI routes
def get_session():
    with Session(engine) as session:
        yield session

class Database:
    @staticmethod
    def init_db():
        create_db_and_tables()