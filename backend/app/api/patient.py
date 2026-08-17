from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.database.connection import get_db, Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text

router = APIRouter()

# Database Model
class PatientDB(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    bmi = Column(Float, nullable=False)
    blood_pressure = Column(Integer, nullable=False)
    medical_history = Column(Text, default="")
    risk_level = Column(String(20), default="Low")
    risk_score = Column(Integer, default=0)
    status = Column(String(30), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Schema
class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    bmi: float
    blood_pressure: int
    medical_history: Optional[str] = ""

class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    bmi: float
    blood_pressure: int
    medical_history: Optional[str]
    risk_level: str
    risk_score: int
    status: str
    created_at: str

@router.post("/", response_model=PatientResponse)
async def create_patient(patient_data: PatientCreate, db: Session = Depends(get_db)):
    # Calculate risk
    risk_score = 0
    if patient_data.bmi > 30:
        risk_score += 40
    elif patient_data.bmi > 25:
        risk_score += 20
        
    if patient_data.blood_pressure > 140:
        risk_score += 40
    elif patient_data.blood_pressure > 120:
        risk_score += 20
    
    if risk_score >= 60:
        risk_level = "High"
    elif risk_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    patient = PatientDB(
        name=patient_data.name,
        age=patient_data.age,
        gender=patient_data.gender,
        bmi=patient_data.bmi,
        blood_pressure=patient_data.blood_pressure,
        medical_history=patient_data.medical_history,
        risk_level=risk_level,
        risk_score=risk_score
    )
    
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    return PatientResponse(
        id=patient.id,
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        bmi=patient.bmi,
        blood_pressure=patient.blood_pressure,
        medical_history=patient.medical_history,
        risk_level=patient.risk_level,
        risk_score=patient.risk_score,
        status=patient.status,
        created_at=patient.created_at.isoformat()
    )

@router.get("/", response_model=List[PatientResponse])
async def get_all_patients(db: Session = Depends(get_db)):
    patients = db.query(PatientDB).order_by(PatientDB.created_at.desc()).all()
    return [
        PatientResponse(
            id=p.id,
            name=p.name,
            age=p.age,
            gender=p.gender,
            bmi=p.bmi,
            blood_pressure=p.blood_pressure,
            medical_history=p.medical_history,
            risk_level=p.risk_level,
            risk_score=p.risk_score,
            status=p.status,
            created_at=p.created_at.isoformat()
        ) for p in patients
    ]