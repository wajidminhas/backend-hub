
from sqlmodel import SQLModel, Session, create_engine
from app import  settings


connection_string  = str (settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg2"
)

engine = create_engine(connection_string, pool_size=300)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session