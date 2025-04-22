# app/main.py
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes.post import router as post_router
from app.routes.user import router as user_router
from contextlib import asynccontextmanager
app = FastAPI(title="Blog API")



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan: starting")
    create_db_and_tables()
    yield
    print("lifespan: shutting down")

app.include_router(post_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}