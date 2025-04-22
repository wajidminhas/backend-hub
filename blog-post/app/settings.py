
from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

# Database settings
DATABASE_URL = config("DATABASE_URL", cast= Secret)