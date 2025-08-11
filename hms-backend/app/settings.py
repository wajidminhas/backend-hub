

# app/settings.py
from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

# Database settings
DATABASE_URL = config("DATABASE_URL", cast=Secret, default="sqlite:///hms.db")  # Default to SQLite
SECRET_KEY = config("SECRET_KEY", cast=Secret, default="your_secret_key_for_jwt")  # For future authentication