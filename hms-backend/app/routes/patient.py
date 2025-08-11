# app/routes/patient.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.models.patient import PatientCreate, PatientResponse
from app.services.patient import PatientService
from app.database import get_session

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=201)
def create_patient(patient_data: PatientCreate, session: Session = Depends(get_session)):
    service = PatientService(session)
    return service.create_patient(patient_data)