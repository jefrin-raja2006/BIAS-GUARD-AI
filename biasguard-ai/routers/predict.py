from fastapi import APIRouter
from pydantic import BaseModel

from services.predict_service import predict_domain

router = APIRouter(prefix="/predict", tags=["Prediction"])


class PatientPredictRequest(BaseModel):
    domain: str
    patient_data: dict


@router.post("/domain")
async def predict_for_patient(req: PatientPredictRequest):
    try:
        result = predict_domain(req.domain, req.patient_data)
        return {"success": True, "data": result}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Prediction failed: {e}"}