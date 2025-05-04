
from starlette.config import Config
from starlette.datastructures import Secret


try:
    config = Config(".env")

except FileNotFoundError:
    raise Exception("Could not find the .env file")


DATABASE_URL = config("DATABASE_URL", cast= Secret)