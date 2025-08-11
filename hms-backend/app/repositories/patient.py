# app/repositories/patient.py
from sqlmodel import Session
from app.models.patient import Patient, PatientCreate

class PatientRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, patient_data: PatientCreate) -> Patient:
        db_patient = Patient(**patient_data.dict(exclude={"medical_history"}))
        self.session.add(db_patient)
        self.session.commit()
        self.session.refresh(db_patient)
        return db_patient