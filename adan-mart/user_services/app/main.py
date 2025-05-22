from typing import Annotated
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager

from sqlmodel import Session
from app import auth
from app.database import create_db_and_tables, get_session
from app.models import Users
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
def greet(name: str):
    return f"hello {name}! Welcome to Adan Mart"

@app.get("/me")
async def user_profile(session: Annotated[Session, Depends(get_session)],
                       current_user : Annotated[Users, Depends(auth.current_user)]
                       ):
    return {"Hello" : "World"}