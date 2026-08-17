from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

# Load .env file
load_dotenv()

# Get credentials
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "biasguard_db")

# Create URL
database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
print(f"Connecting to: mysql+pymysql://{db_user}:****@{db_host}:{db_port}/{db_name}")

try:
    engine = create_engine(database_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        print(f"✅ Connected to: {db_name}")
except Exception as e:
    print(f"❌ Error: {e}")