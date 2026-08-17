from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=0, le=150)
    gender: GenderEnum
    bmi: float = Field(..., ge=10, le=50)
    blood_pressure: int = Field(..., ge=80, le=200)
    medical_history: Optional[str] = ""
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

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
    created_at: datetime
    updated_at: datetime

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    bmi: Optional[float] = None
    blood_pressure: Optional[int] = None
    medical_history: Optional[str] = None
    status: Optional[str] = None