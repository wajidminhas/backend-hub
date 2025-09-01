from sqlmodel import create_engine, SQLModel, Session
from app import settings
# from app.models import User, Post  # Import models

connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_string, echo=True)


def create_db_and_tables():
    print("Creating tables...")
    try:
        SQLModel.metadata.create_all(engine)
        print("Tables created successfully: user, post")
    except Exception as e:
        print(f"Table creation failed: {e}")
        raise

def create_session():
    with Session(engine) as session:
        yield session