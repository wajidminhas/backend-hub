


from typing import Annotated

from fastapi.params import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from sqlalchemy.orm import Session

from app.dependencies import get_db


class Settings(BaseSettings):
    database_url : str
    DbSession : Annotated[Session, Depends(get_db)]
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )
    
settings = Settings()

