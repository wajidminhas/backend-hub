


from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    db_engine: str = "postgresql+pscyopg2"
    db_user : str
    db_password : str
    db_host: str
    db_port: int
    db_name: str 
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )
    
settings = Settings()

