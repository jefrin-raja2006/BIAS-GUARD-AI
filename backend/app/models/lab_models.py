from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class LabReport(Base):
    __tablename__ = "lab_reports"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False)
    test_date = Column(DateTime, nullable=False)
    notes = Column(Text, default="")
    
    blood_glucose = Column(Float, nullable=True)
    cholesterol = Column(Float, nullable=True)
    hemoglobin = Column(Float, nullable=True)
    
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="lab_reports")
    uploader = relationship("User", foreign_keys=[uploaded_by])
    
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "file_name": self.file_name,
            "file_url": self.file_url,
            "file_type": self.file_type,
            "test_date": self.test_date.isoformat() if self.test_date else None,
            "notes": self.notes,
            "blood_glucose": self.blood_glucose,
            "cholesterol": self.cholesterol,
            "hemoglobin": self.hemoglobin,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }