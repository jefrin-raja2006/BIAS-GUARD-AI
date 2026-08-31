from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from clinical_standardization.service import (
    standardize_clinical_parameters
)


router = APIRouter(
    prefix="/clinical",
    tags=["Clinical Standardization"]
)


class ClinicalParameter(BaseModel):
    original_name: str
    value: Any
    unit: str = ""
    reference_range: str = ""
    canonical_feature_id: str = ""
    canonical_feature_name: str = ""
    match_status: str = "REVIEW_REQUIRED"
    confidence_score: float = 0


class StandardizationRequest(BaseModel):
    parameters: List[ClinicalParameter]


@router.post("/standardize")
def standardize_clinical_data(
    request: StandardizationRequest
):
    try:
        parameters = [
            parameter.model_dump()
            for parameter in request.parameters
        ]

        result = standardize_clinical_parameters(
            parameters
        )

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to standardize clinical parameters: "
                f"{str(error)}"
            )
        )