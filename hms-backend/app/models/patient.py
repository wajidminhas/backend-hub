# app/models/patient.py
from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class PatientBase(SQLModel):
    name: str = Field(index=True)
    email: Optional[str] = Field(unique=True, index=True, nullable=True)
    phone: Optional[str] = Field(nullable=True)
    date_of_birth: Optional[datetime] = Field(nullable=True)
    address: Optional[dict] = Field(default=None, sa_type=SQLModel.JSON)  # JSON for flexibility
    emergency_contact: Optional[str] = Field(nullable=True)

class Patient(PatientBase, table=True):
    patient_id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

class PatientCreate(PatientBase):
    medical_history: Optional[List[dict]] = Field(default=None, sa_type=SQLModel.JSON)

class PatientResponse(Patient):
    medical_history: Optional[List[dict]] = Field(default=None)

class MedicalHistory(SQLModel, table=True):
    history_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.patient_id")
    condition: str
    diagnosed_date: Optional[datetime] = Field(nullable=True)
    treatment: Optional[str] = Field(nullable=True)
    notes: Optional[str] = Field(nullable=True)