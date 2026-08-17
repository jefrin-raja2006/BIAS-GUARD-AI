from sqlalchemy import create_engine, text
import pymysql

# Test MySQL connection
try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='punas',
        database='biasguard_db',
        port=3306
    )
    print("✅ MySQL connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
