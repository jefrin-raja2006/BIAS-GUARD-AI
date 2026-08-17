from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='kiki',
        database='biasguard_db',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Patient model
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
        
        # Calculate risk
        risk_score = 0
        if patient.bmi > 30:
            risk_score += 40
        elif patient.bmi > 25:
            risk_score += 20
        if patient.blood_pressure > 140:
            risk_score += 40
        elif patient.blood_pressure > 120:
            risk_score += 20
        
        risk_level = "High" if risk_score >= 60 else "Medium" if risk_score >= 30 else "Low"
        status = 'lab_required' if risk_level == 'High' else 'pending'
        
        sql = """
            INSERT INTO patients (name, age, gender, bmi, blood_pressure, medical_history, risk_level, risk_score, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            patient.name, patient.age, patient.gender, patient.bmi,
            patient.blood_pressure, patient.medical_history, risk_level, risk_score, status
        ))
        conn.commit()
        patient_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            result['created_at'] = str(result['created_at'])
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
                try:
                    patient['lab_results'] = json.loads(patient['lab_results'])
                except:
                    pass
            if patient.get('prediction') and isinstance(patient['prediction'], str):
                try:
                    patient['prediction'] = json.loads(patient['prediction'])
                except:
                    pass
        
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
                try:
                    patient['lab_results'] = json.loads(patient['lab_results'])
                except:
                    patient['lab_results'] = None
            if patient.get('prediction') and isinstance(patient['prediction'], str):
                try:
                    patient['prediction'] = json.loads(patient['prediction'])
                except:
                    patient['prediction'] = None
        
        return {"success": True, "data": patients}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/patients/lab")
async def get_lab_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM patients 
            WHERE status = 'lab_required'
            ORDER BY created_at DESC
        """)
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
                try:
                    patient['lab_results'] = json.loads(patient['lab_results'])
                except:
                    pass
            if patient.get('prediction') and isinstance(patient['prediction'], str):
                try:
                    patient['prediction'] = json.loads(patient['prediction'])
                except:
                    pass
            return {"success": True, "data": patient}
        else:
            return {"success": False, "error": "Patient not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== LAB ENDPOINTS ====================

@app.post("/api/lab/upload")
async def upload_lab_results(
    file: UploadFile = File(...),
    patient_id: int = Form(...)
):
    try:
        # Validate file type
        allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if file.content_type not in allowed_types:
            return {"success": False, "error": "Only PDF and DOCX files are allowed"}
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        lab_data = {
            "filename": file.filename,
            "saved_as": unique_filename,
            "file_type": file.content_type,
            "file_url": f"/uploads/{unique_filename}",
            "uploaded_at": datetime.utcnow().isoformat()
        }
        
        # Convert to JSON string for storage
        lab_results_json = json.dumps(lab_data)
        
        cursor.execute("""
            UPDATE patients 
            SET status = 'lab_uploaded', lab_results = %s 
            WHERE id = %s
        """, (lab_results_json, patient_id))
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Lab results uploaded successfully", "data": lab_data}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== PREDICTION ENDPOINTS ====================

# Replace your existing @app.post("/api/predictions/{patient_id}") function
# in app\main.py with this version.

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

        # Lab data is mandatory before final prediction (per workflow: Stage 2
        # requires lab reports). Refuse instead of faking a result.
        if not patient.get('lab_results'):
            conn.close()
            return {
                "success": False,
                "error": "Lab report required. This patient has no lab_results on file yet."
            }

        try:
            lab_results = json.loads(patient['lab_results']) if isinstance(patient['lab_results'], str) else patient['lab_results']
        except Exception:
            conn.close()
            return {"success": False, "error": "lab_results is not valid JSON"}

        # Merge patient demographics (already collected by nurse) with
        # disease-specific lab values (entered by lab technician), using the
        # exact field names the models expect.
        patient_data = {
            "Age": patient['age'],
            "BMI": patient['bmi'],
            "BloodPressure": patient['blood_pressure'],
        }
        patient_data.update(lab_results)

        # Call the real BiasGuard AI prediction engine on port 8002
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    "http://localhost:8002/predict/domain",
                    json={"domain": "endocrinology", "patient_data": patient_data},
                    timeout=30.0
                )
                predict_response = r.json()
        except Exception as e:
            conn.close()
            return {"success": False, "error": f"BiasGuard prediction backend unavailable: {e}"}

        if not predict_response.get("success"):
            conn.close()
            return {"success": False, "error": predict_response.get("error", "Prediction failed")}

        domain_result = predict_response["data"]
        results = domain_result.get("results", [])

        if not results:
            conn.close()
            return {
                "success": False,
                "error": "No disease model had enough lab data to predict. Missing fields per disease are listed.",
                "skipped": domain_result.get("skipped", [])
            }

        # Top-ranked result becomes the headline prediction; full ranked list
        # and skipped diseases are kept for transparency in the UI.
        top = results[0]
        disease_name_map = {
            "diabetes": "Type 2 Diabetes",
            "thyroid": "Thyroid Disorder",
            "glucose": "Glucose Disorder",
            "pcos": "PCOS",
            "malnutrition": "Malnutrition",
            "vitamin_d": "Vitamin D Deficiency",
            "obesity": "Obesity",
            "metabolic": "Metabolic Disorder",
        }

        prediction = {
            "disease": disease_name_map.get(top["disease"], top["disease"]),
            "confidence": top["confidence"],
            "risk_score": patient['risk_score'],
            "all_results": results,
            "skipped_diseases": domain_result.get("skipped", []),
            "recommendations": [
                "Immediate consultation recommended",
                "Further tests required",
                "Follow-up in 2 weeks"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }

        prediction_json = json.dumps(prediction)
        cursor.execute("""
            UPDATE patients SET prediction = %s, status = 'DIAGNOSIS_COMPLETED' WHERE id = %s
        """, (prediction_json, patient_id))
        conn.commit()
        conn.close()

        return {"success": True, "data": prediction}
    except Exception as e:
        return {"success": False, "error": str(e)}

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
