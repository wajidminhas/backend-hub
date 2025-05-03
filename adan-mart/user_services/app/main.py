from fastapi import FastAPI

from app import auth




app = FastAPI(title= "User Service")
# app.include_router(auth.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def greet (name):
    return f"hello {name}! Welcome to Adan Mart"