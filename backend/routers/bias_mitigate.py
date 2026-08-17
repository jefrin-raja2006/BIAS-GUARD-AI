from fastapi import APIRouter, Query, HTTPException
from services.mitigation_service import run_smote, run_synthetic
from disease_config import SUPPORTED_DISEASES

router = APIRouter(prefix="/mitigate", tags=["Bias Mitigation"])


@router.post("/smote")
def mitigate_smote(
    disease: str = Query(
        ...,
        description=f"Disease to apply SMOTE on. Supported: {SUPPORTED_DISEASES}",
        example="diabetes"
    )
):
    """
    Apply SMOTE (Synthetic Minority Over-sampling Technique) to balance
    the disease dataset across class labels.

    Returns before/after class distribution and number of samples added.
    """
    try:
        result = run_smote(disease)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SMOTE failed: {str(e)}")


@router.post("/synthetic")
def mitigate_synthetic(
    disease: str = Query(
        ...,
        description=f"Disease to generate synthetic data for. Supported: {SUPPORTED_DISEASES}",
        example="diabetes"
    ),
    num_rows: int = Query(
        default=200,
        ge=10,
        le=2000,
        description="Number of synthetic rows to generate"
    )
):
    """
    Generate synthetic patient records using GaussianCopulaSynthesizer (SDV)
    to augment underrepresented groups.

    Returns synthetic group distribution, target distribution, and a 5-row preview.
    """
    try:
        result = run_synthetic(disease, num_rows=num_rows)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synthetic generation failed: {str(e)}")