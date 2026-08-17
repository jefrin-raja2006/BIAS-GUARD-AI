from app.database.connection import init_db, SessionLocal
from app.models.user_model import User, UserRole
from app.models.patient_model import Patient

def create_initial_users():
    """Create initial users for testing"""
    db = SessionLocal()
    
    # Check if users already exist
    if db.query(User).count() == 0:
        users = [
            User(
                username="nurse",
                name="Sarah Johnson",
                role=UserRole.NURSE,
                email="nurse@biasguard.com"
            ),
            User(
                username="lab",
                name="Mike Chen",
                role=UserRole.LAB,
                email="lab@biasguard.com"
            ),
            User(
                username="doctor",
                name="Dr. Jefrin",
                role=UserRole.DOCTOR,
                email="doctor@biasguard.com"
            )
        ]
        
        for user in users:
            user.hash_password("password123")
            db.add(user)
        
        db.commit()
        print("✅ Initial users created successfully")
    
    db.close()

if __name__ == "__main__":
    print("🚀 Initializing database...")
    init_db()
    create_initial_users()
    print("✅ Database initialization complete!")