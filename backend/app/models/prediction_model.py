from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, unique=True)
    disease = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    risk_score = Column(Integer, nullable=False)
    recommendations = Column(JSON, default=list)
    bias_detected = Column(Boolean, default=False)
    bias_report = Column(JSON, nullable=True)
    doctor_notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="prediction")
    
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "disease": self.disease,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "recommendations": self.recommendations,
            "bias_detected": self.bias_detected,
            "bias_report": self.bias_report,
            "doctor_notes": self.doctor_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }