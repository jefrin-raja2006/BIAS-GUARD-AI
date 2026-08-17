from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
import pymysql
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import os
import shutil
import uuid
import json
import httpx

app = FastAPI(title="BiasGuard AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='kiki',
        database='biasguard_db',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ==================== AUTH ====================

class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND role = %s",
            (request.username, request.role.upper())
        )
        user = cursor.fetchone()
        conn.close()

        if not user:
            return {"success": False, "error": "Invalid credentials"}

        if not pwd_context.verify(request.password, user['password']):
            return {"success": False, "error": "Invalid credentials"}

        return {"success": True, "data": {
            "id": user['id'],
            "username": user['username'],
            "role": user['role']
        }}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== PATIENT MODEL ====================

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    bmi: float
    blood_pressure: int
    medical_history: Optional[str] = ""

@app.get("/")
async def root():
    return {"message": "BiasGuard AI API is running", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# ==================== PATIENT ENDPOINTS ====================

@app.post("/api/patients")
async def create_patient(patient: PatientCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        risk_score = 0
        if patient.bmi > 30: risk_score += 40
        elif patient.bmi > 25: risk_score += 20
        if patient.blood_pressure > 140: risk_score += 40
        elif patient.blood_pressure > 120: risk_score += 20
        risk_level = "High" if risk_score >= 60 else "Medium" if risk_score >= 30 else "Low"
        status = 'LAB_REQUIRED' if risk_level == 'High' else 'PENDING'
        sql = """
            INSERT INTO patients (name, age, gender, bmi, blood_pressure, medical_history, risk_level, risk_score, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (patient.name, patient.age, patient.gender, patient.bmi,
            patient.blood_pressure, patient.medical_history, risk_level, risk_score, status))
        conn.commit()
        patient_id = cursor.lastrowid
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        result = cursor.fetchone()
        conn.close()
        if result: result['created_at'] = str(result['created_at'])
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/patients")
async def get_all_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
        patients = cursor.fetchall()
        conn.close()
        for patient in patients:
            patient['created_at'] = str(patient['created_at'])
            if patient.get('lab_results') and isinstance(patient['lab_results'], str):
                try: patient['lab_results'] = json.loads(patient['lab_results'])
                except: pass
            if patient.get('prediction') and isinstance(patient['prediction'], str):
                try: patient['prediction'] = json.loads(patient['prediction'])
                except: pass
        return {"success": True, "data": patients}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/patients/doctor")
async def get_doctor_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
        patients = cursor.fetchall()
        conn.close()
        for patient in patients:
            patient['created_at'] = str(patient['created_at'])
            if patient.get('lab_results') and isinstance(patient['lab_results'], str):
                try: patient['lab_results'] = json.loads(patient['lab_results'])
                except: patient['lab_results'] = None
            if patient.get('prediction') and isinstance(patient['prediction'], str):
                try: patient['prediction'] = json.loads(patient['prediction'])
                except: patient['prediction'] = None
        return {"success": True, "data": patients}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/patients/lab")
async def get_lab_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE status = 'LAB_REQUIRED' ORDER BY created_at DESC")
        patients = cursor.fetchall()
        conn.close()
        for patient in patients:
            patient['created_at'] = str(patient['created_at'])
        return {"success": True, "data": patients}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/patients/lab/all")
async def get_all_lab_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
        patients = cursor.fetchall()
        conn.close()
        for patient in patients:
            patient['created_at'] = str(patient['created_at'])
        return {"success": True, "data": patients}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/patients/{patient_id}")
async def get_patient(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()
        conn.close()
        if patient:
            patient['created_at'] = str(patient['created_at'])
            if patient.get('lab_results') and isinstance(patient['lab_results'], str):
                try: patient['lab_results'] = json.loads(patient['lab_results'])
                except: pass
            if patient.get('prediction') and isinstance(patient['prediction'], str):
                try: patient['prediction'] = json.loads(patient['prediction'])
                except: pass
            return {"success": True, "data": patient}
        return {"success": False, "error": "Patient not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== LAB ENDPOINTS ====================

@app.post("/api/lab/upload")
async def upload_lab_results(file: UploadFile = File(...), patient_id: int = Form(...)):
    try:
        allowed_types = ['application/pdf', 'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if file.content_type not in allowed_types:
            return {"success": False, "error": "Only PDF and DOCX files are allowed"}
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        conn = get_db_connection()
        cursor = conn.cursor()
        lab_data = {
            "filename": file.filename, "saved_as": unique_filename,
            "file_type": file.content_type, "file_url": f"/uploads/{unique_filename}",
            "uploaded_at": datetime.utcnow().isoformat()
        }
        cursor.execute(
            "UPDATE patients SET prediction = %s, status = 'DIAGNOSIS_COMPLETED' WHERE id = %s"
            (json.dumps(lab_data), patient_id)
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": "Lab results uploaded successfully", "data": lab_data}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== PREDICTION ENDPOINTS ====================

@app.post("/api/predictions/{patient_id}")
async def generate_prediction(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()
        if not patient:
            conn.close()
            return {"success": False, "error": "Patient not found"}
        if not patient.get('lab_results'):
            conn.close()
            return {"success": False, "error": "Lab report required."}
        try:
            lab_results = json.loads(patient['lab_results']) if isinstance(patient['lab_results'], str) else patient['lab_results']
        except:
            conn.close()
            return {"success": False, "error": "lab_results is not valid JSON"}
        patient_data = {"Age": patient['age'], "BMI": patient['bmi'], "BloodPressure": patient['blood_pressure']}
        patient_data.update(lab_results)
        async with httpx.AsyncClient() as client:
            r = await client.post(
                "http://localhost:8002/predict/domain",
                json={"domain": "endocrinology", "patient_data": patient_data},
                timeout=30.0
            )
            predict_response = r.json()
        if not predict_response.get("success"):
            conn.close()
            return {"success": False, "error": predict_response.get("error", "Prediction failed")}
        domain_result = predict_response["data"]
        results = domain_result.get("results", [])
        if not results:
            conn.close()
            return {"success": False, "error": "No disease model had enough lab data to predict."}
        top = results[0]
        disease_name_map = {
            "diabetes": "Type 2 Diabetes", "thyroid": "Thyroid Disorder",
            "glucose": "Glucose Disorder", "pcos": "PCOS",
            "malnutrition": "Malnutrition", "vitamin_d": "Vitamin D Deficiency",
            "obesity": "Obesity", "metabolic": "Metabolic Disorder",
        }
        prediction = {
            "disease": disease_name_map.get(top["disease"], top["disease"]),
            "confidence": top["confidence"],
            "risk_score": patient['risk_score'],
            "all_results": results,
            "skipped_diseases": domain_result.get("skipped", []),
            "recommendations": ["Immediate consultation recommended", "Further tests required", "Follow-up in 2 weeks"],
            "timestamp": datetime.utcnow().isoformat()
        }
        cursor.execute(
            "UPDATE patients SET prediction = %s, status = 'DIAGNOSIS_COMPLETED' WHERE id = %s",
            (json.dumps(prediction), patient_id)
        )
        conn.commit()
        conn.close()
        return {"success": True, "data": prediction}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)