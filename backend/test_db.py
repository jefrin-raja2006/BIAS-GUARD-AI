from app.config import settings
from app.database.connection import engine, init_db

print("Testing database connection...")
print(f"Database URL: {settings.DATABASE_URL}")

try:
    # Test connection
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ Database connection successful!")
        
    # Initialize tables
    init_db()
    print("✅ Tables created successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")