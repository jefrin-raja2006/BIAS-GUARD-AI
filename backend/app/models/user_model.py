from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from passlib.context import CryptContext
from app.database.connection import Base
import enum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRole(str, enum.Enum):
    NURSE = "nurse"
    LAB = "lab"
    DOCTOR = "doctor"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def hash_password(self, password: str):
        """Hash password before storing"""
        self.password = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(password, self.password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "role": self.role.value if self.role else None,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }