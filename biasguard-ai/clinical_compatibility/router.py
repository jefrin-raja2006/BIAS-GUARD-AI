# clinical_compatibility/router.py

from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel, Field

from clinical_compatibility.service import check_model_compatibility


router = APIRouter(
    prefix="/clinical/compatibility",
    tags=["Clinical Compatibility"]
)


class CompatibilityRequest(BaseModel):
    standardized_features: Dict[str, Any] = Field(
        ...,
        description="Standardized clinical features from Phase 2"
    )


@router.post("/check")
def check_compatibility(request: CompatibilityRequest):
    """
    Check standardized clinical features against all
    registered disease prediction models.
    """

    result = check_model_compatibility(
        request.standardized_features
    )

    return result