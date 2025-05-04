from fastapi import FastAPI
from contextlib import asynccontextmanager
from app import auth
from app.database import create_db_and_tables
from app.router.user import user_router




@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan: starting")
    create_db_and_tables()
    yield
    print("lifespan: shutting down")

    # Code to run when the application stops
app = FastAPI(
    lifespan=lifespan,
    title= "User Service")
# app.include_router(auth.router)
app.include_router(router=user_router)

@app.get("/")
def greet (name):
    return f"hello {name}! Welcome to Adan Mart"