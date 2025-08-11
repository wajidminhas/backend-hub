# app/services/patient.py
from app.models.patient import Patient, PatientCreate
from app.repositories.patient import PatientRepository

class PatientService:
    def __init__(self, session):
        self.repository = PatientRepository(session)

    def create_patient(self, patient_data: PatientCreate) -> Patient:
        # Add business logic (e.g., validate email uniqueness)
        return self.repository.create(patient_data)