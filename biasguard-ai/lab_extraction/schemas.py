from pydantic import BaseModel, Field
from typing import Optional, List


class ExtractedParameter(BaseModel):
    original_name: str
    original_value: Optional[float] = None
    original_unit: Optional[str] = ""
    reference_range: Optional[str] = ""

    canonical_feature_id: Optional[str] = ""
    canonical_feature_name: Optional[str] = ""
    database_feature_name: Optional[str] = ""

    match_status: str = "REVIEW_REQUIRED"
    match_method: str = "REVIEW_REQUIRED"
    confidence_score: float = 0.0

    unit_status: str = "REVIEW_REQUIRED"

    standardized_value: Optional[float] = None
    standardized_unit: Optional[str] = ""


class ExtractionResult(BaseModel):
    extracted_parameters: List[ExtractedParameter] = []
    unmatched_parameters: List[str] = []

    total_extracted: int = 0
    matched: int = 0
    review_required: int = 0


class LabExtractionResponse(BaseModel):
    success: bool
    filename: str
    extracted_text: str
    data: ExtractionResult