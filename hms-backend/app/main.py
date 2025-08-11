

# app/main.py
from fastapi import FastAPI
from app.database import Database
from app.routes.patient import router as patient_router

app = FastAPI(title="Hospital Management System")

app.include_router(patient_router)

@app.on_event("startup")
def startup_event():
    Database.init_db()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}