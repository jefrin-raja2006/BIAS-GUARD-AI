from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from disease_prediction.service import run_disease_predictions


router = APIRouter(
    prefix="/disease",
    tags=["Disease Prediction"]
)


# ==========================================================
# REQUEST MODEL
# ==========================================================

class DiseasePredictionRequest(BaseModel):
    standardized_features: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Clinically standardized features from BiasGuard"
    )


# ==========================================================
# RESPONSE ENDPOINT
# ==========================================================

@router.post("/predict")
def predict_diseases(request: DiseasePredictionRequest):
    """
    Run compatible Endocrinology disease prediction models.

    Prediction is performed only when all features required
    by a trained model are available.
    """

    try:

        result = run_disease_predictions(
            request.standardized_features
        )

        return result

    except Exception as e:

        print(
            f"[BiasGuard AI] Disease prediction error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Disease prediction failed: {str(e)}"
        )