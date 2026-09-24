

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import  sessionmaker, declarative_base
from app.config import settings



# connection_url = URL.create(
#     drivername=settings.db_engine,
#     username=settings.db_user,
#     password=settings.db_password,
#     host=settings.db_host, 
#     port=settings.db_port,
#     database=settings.db_name
# )

engine = create_engine(settings.database_url, echo=True)


SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()