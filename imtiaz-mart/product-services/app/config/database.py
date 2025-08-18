

from sqlmodel import SQLModel, create_engine, Session
from app import settings
from sqlmodel.ext.asyncio import AsyncSession, sessionmaker
from app.settings import settings


connection_str = settings(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")


engine = create_engine(
    connection_str,
    echo=settings(settings.DEBUG),
    future=True,
)

async def create_db_table():
    """Create the database tables."""
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    """Get a new async SQLModel session."""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
