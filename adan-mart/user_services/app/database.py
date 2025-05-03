

from sqlmodel import SQLModel, Session, create_engine
from app import settings
from app.models import Users


connection_str = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")


engine = create_engine(connection_str, echo=True)


def create_db_and_tables():
    """Create the database and tables."""
    # Create the database and tables
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a session to the database."""
    with Session(engine) as session:
        yield session