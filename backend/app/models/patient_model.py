from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base
import enum

class PatientStatus(str, enum.Enum):
    PENDING = "pending"
    LAB_REQUIRED = "lab_required"
    LAB_UPLOADED = "lab_uploaded"
    DIAGNOSIS_COMPLETED = "diagnosis_completed"

class RiskLevel(str, enum.Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    bmi = Column(Float, nullable=False)
    blood_pressure = Column(Integer, nullable=False)
    medical_history = Column(Text, default="")
    
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW)
    risk_score = Column(Integer, default=0)
    status = Column(Enum(PatientStatus), default=PatientStatus.PENDING)
    
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender.value if self.gender else None,
            "bmi": self.bmi,
            "blood_pressure": self.blood_pressure,
            "medical_history": self.medical_history,
            "risk_level": self.risk_level.value if self.risk_level else None,
            "risk_score": self.risk_score,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }